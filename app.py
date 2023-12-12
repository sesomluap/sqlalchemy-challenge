# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, request, jsonify
import datetime as dt


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

# Calculate the date one year from the last date in data set.
prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

#create landing page
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/dates<br/>"
        f"to enter a date range, add: ?start=YYYY-MM-DD&end=YYYY-MM-DD<br/>"
        f"end date may be omitted"
        
    )

#first route shows final year precipitation data
@app.route("/api/v1.0/precipitation")
def precip():
    """Show precipitation data over last year"""
    #Query the final year of precipitation data
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()
    
    #create a dictionary for the row data and append to a list
    rain = []
    for date, prcp in results:
        rain_dict = {}
        rain_dict['date'] = date
        rain_dict['prcp'] = prcp
        rain.append(rain_dict)
    
    #convert to JSON
    return jsonify(rain)

#Create a route for station data
@app.route("/api/v1.0/stations")
def stations():
    """List all stations"""
    #Query station data
    res = session.query(Station.station, Station.name).all()

    #Create a list from the results
    all_stations = list(np.ravel(res))

    #convert list to JSON
    return jsonify(all_stations)

#Create a route for final year temperature data from the most active station
@app.route("/api/v1.0/tobs")
def tobs():
    """List temperature from most active station over last year"""
    #Query final year termperature data
    temp = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= prev_year).\
        filter(Measurement.station == 'USC00519281').all()

    #Create a list from the data
    yr_temp = list(np.ravel(temp))

    #Convert to JSON
    return jsonify(yr_temp)

#Create a route to find min/max/avg temperatures by date range
@app.route("/api/v1.0/dates", methods=['GET'])
def calc_temp():
    """List min/max/mean temperature for a date range"""
    
    #retrieve start and end dates
    start = request.args.get('start')
    end = request.args.get('end')

    # Validate start date input and provide prompt if necessary
    if not start:
        return {"error": "Please provide the 'start' date as a query parameter."}

    try:
        start_date = dt.datetime.strptime(start, '%Y-%m-%d').date()
    except ValueError:
        return {"error": "Invalid 'start' date format. Please use 'YYYY-MM-DD'."}

    # Validate end date input and provide prompt if necessary
    if end:
        try:
            end_date = dt.datetime.strptime(end, '%Y-%m-%d').date()
        except ValueError:
            return {"error": "Invalid 'end' date format. Please use 'YYYY-MM-DD'."}
    else:
        # Set default end date to the maximum date in the dataset
        end_date = dt.date(2017, 8, 23)

    # Request temperature data
    filtered_data = session.query(Measurement.date, Measurement.tobs)

    #filter by start date
    if start_date:
        filtered_data = filtered_data.filter(Measurement.date >= start_date)

    #filter by end date
    if end_date:
        filtered_data = filtered_data.filter(Measurement.date <= end_date)

    #collect filtered results and provide prompt if necessary
    data = filtered_data.all()

    if not data:
        return {"error": "No data available for the specified date range."}

    #find max/min/avg temp
    min_temp = min(entry.tobs for entry in data)
    avg_temp = sum(entry.tobs for entry in data) / len(data)
    max_temp = max(entry.tobs for entry in data)

    #return the values
    output = {"min_temp": min_temp, "avg_temp": avg_temp, "max_temp": max_temp}
    
    #convert to JSON
    return jsonify(output)

#run the app
if __name__ == "__main__":
    app.run(debug=True)
