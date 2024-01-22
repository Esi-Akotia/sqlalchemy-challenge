# sqlalchemy-challenge

This repo contains a Resource folder with csv files and a sqlite file which are the key sources of analysis run.
In the SurfsUp folder, you will find a Jupyter Notebook and a Python file with the full analysis script. 
For this challenge, I searched online for assistance on sections of the code from Stack Overflow and ChatGPT. Find them below:

```year_before = most_recent_date - relativedelta(years=1)``` -- Using relativedelta to get the previous year's date
```plt.xticks(range(0, len(df['Date']), max(1, len(df['Date']) // 10)),``` -- To evenly distributed tick steps for bar graph
```df['Date'][::max(1, len(df['Date']) // 10)].dt.strftime('%Y-%m-%d'))``` -- To create a subset of dates converted to datetime format


           