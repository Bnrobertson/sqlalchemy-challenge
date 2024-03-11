# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# Declare a Base using `automap_base()`
Base = automap_base()
# Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session
session = Session(engine)

# #################################################
# # Flask Setup
# #################################################
app = Flask(__name__)



# #################################################
# # Flask Routes
# #################################################
@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<br/>"
        f"/api/v1.0/temp/start/end<br/>"
        f"<p>'start' and 'end' date should be in the format MMDDYYYY.</p>")
#Convert the query results from your precipitation analysis
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Calculate the date 1 year ago from the last data point in the database
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    most_recent_date = dt.datetime.strptime(most_recent_date[0], '%Y-%m-%d')
    one_year_ago = most_recent_date - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).all()

    # Convert the query results to a dictionary with date as the key and prcp as the value
    formatted_data = {date: prcp for date, prcp in results}

    return jsonify(formatted_data)

#Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    # Query all station names
    station_names = session.query(Station.station).all()

    # Convert the list of tuples to a list of station names
    station_list = [name[0] for name in station_names]

    return jsonify(station_list)

#Query the dates and temperature observations of the most-active 
# station for the previous year of data.
@app.route("/api/v1.0/tobs")
def tobs():
    # Query the most active station using a subquery
    most_active_station = session.query(Measurement.station,
                         func.count(Measurement.station).label('count')) \
                        .group_by(Measurement.station) \
                        .order_by(func.count(Measurement.station).desc()) \
                        .first()[0]

    # Query the date and temperature observations for the most active station for the last year
    last_year_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(Measurement.date, Measurement.tobs) \
            .filter(Measurement.station == most_active_station) \
            .filter(Measurement.date >= last_year_date) \
            .all()

    # Convert the result into a list of dictionaries for JSON serialization
    tobs_data = []
    for date, tobs in results:
        tobs_data.append({
            "date": date,
            "temperature": tobs
        })

    return jsonify(tobs_data)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def temps_start(start=None, end=None):
    """Return TMIN, TAVG, TMAX."""
    # Select statement
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    if not end:
        start = dt.datetime.strptime(start, "%m%d%Y")
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        session.close()
        temps = list(np.ravel(results))
        return jsonify(temps)
    # calculate TMIN, TAVG, TMAX with start and stop
    start = dt.datetime.strptime(start, "%m%d%Y")
    end = dt.datetime.strptime(end, "%m%d%Y")
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    session.close()
    # Unravel results into a 1D array and convert to a list
    temps = list(np.ravel(results))
    return jsonify(temps=temps)



#Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
