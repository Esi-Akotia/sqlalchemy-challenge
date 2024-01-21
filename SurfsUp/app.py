# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy.sql import and_
from dateutil.relativedelta import relativedelta

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

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
# QQ - station ID or station NAME?! ----------------------------------------------------- 
all_stations = session.query(Station.name).all()
all_stations_list = [station[0] for station in all_stations]

# Dates and temperature observations of the most-active station for the previous year 
last_12_months_temp_data = session.query(Measurement.date, Measurement.tobs)\
    .filter(and_(Measurement.date >= year_before, Measurement.date <= most_recent_date))\
    .filter(Measurement.station == 'USC00519281')\
    .order_by(Measurement.tobs).all()
temperatures = [temp[0] for temp in last_12_months_temp_data]

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

if __name__ == "__main__":
    app.run(debug=True)