# Import the dependencies.
import os
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy.sql import and_
import datetime as dt
from dateutil.relativedelta import relativedelta

#################################################
# Database Setup
#################################################
# Get the absolute path to the directory containing this script
current_directory = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to the SQLite database file
database_path = os.path.join(current_directory, "Resources", "hawaii.sqlite")

# Create the engine with the absolute path
engine = create_engine(f"sqlite:///{database_path}")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Convert precipitation query results to dictionary
most_recent_date = session.query(func.max(Measurement.date)).scalar()
most_recent_date = dt.datetime.strptime(most_recent_date, '%Y-%m-%d')
year_before = most_recent_date - relativedelta(years=1)
last_12_months_data = session.query(Measurement.date, Measurement.prcp)\
    .filter(and_(Measurement.date >= year_before, Measurement.date <= most_recent_date))\
    .all()
precipitation_results = {result.date: result.prcp for result in last_12_months_data}

# List of stations  
all_stations = session.query(Station.name).all()
all_stations_list = [station[0] for station in all_stations]

# Dates and temperature observations of the most-active station for the previous year 
last_12_months_temp_data = session.query(Measurement.date, Measurement.tobs)\
    .filter(and_(Measurement.date >= year_before, Measurement.date <= most_recent_date))\
    .filter(Measurement.station == 'USC00519281')\
    .order_by(Measurement.tobs).all()
temperatures = [temp[1] for temp in last_12_months_temp_data]

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def homepage():
    return (
        f"Welcome to Esi's Climate App!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
        )

@app.route("/api/v1.0/precipitation")
def precipitation():
    return jsonify (precipitation_results)

@app.route("/api/v1.0/stations")
def stations():
    return jsonify (all_stations_list)

@app.route("/api/v1.0/tobs")
def temperature_obs():
    return jsonify (temperatures)

@app.route("/api/v1.0/<start>")
def specified_start(start):
    
    # Convert the start parameter to a datetime object
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    
    # Query the minimum, maximum, and average temperature for dates greater than or equal to the start date
    start_values = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))\
    .filter(Measurement.date >= start_date).all()
    
     # Extract the values from the query result
    min_temp, max_temp, avg_temp = start_values[0]

    # Create a dictionary to hold the results
    start_results = {
        "min_temperature": min_temp,
        "max_temperature": max_temp,
        "avg_temperature": avg_temp
        }
    return jsonify (start_results)

@app.route("/api/v1.0/<start>/<end>")
def specified_range(start, end):
    # Convert the start and end parameters to datetime objects
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    end_date = dt.datetime.strptime(end, '%Y-%m-%d')

    range_values = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))\
    .filter(and_(Measurement.date >= start_date, Measurement.date <= end_date)).all()

    # Extract the values from the query result
    min_temp, max_temp, avg_temp = range_values[0]

    # Create a dictionary to hold the results
    range_results = {
        "min_temperature": min_temp,
        "max_temperature": max_temp,
        "avg_temperature": avg_temp
    }
    return jsonify (range_results)

if __name__ == "__main__":
    app.run(debug=True)