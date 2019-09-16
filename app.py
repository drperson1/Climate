import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func

from flask import Flask, jsonify
  
###########################################
#Database Setup
###########################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
   
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
 
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB\
session = Session(engine)

##########################################
# Flask Setup
##########################################

app = Flask(__name__)


##########################################
# Flask Routes
##########################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a dictionary of last twelves months of precipitation scores"""
    # Query all precipitation scoress
    prcp_data_results=session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date>'2016-08-23').filter(Measurement.date<'2017-08-24').\
    order_by(Measurement.date.desc()).all()

        # Create a dictionary from the row data and append to a list of all precipitation scores
    all_prcp_scores = []
    for row in prcp_data_results:
    #     print("row", row)
    #     print(row.date, row.prcp)
        prcp_dict = {"date" : row.date, "prcp": row.prcp}
        all_prcp_scores.append(prcp_dict)

    # Return json representation of dictionary                 
    return jsonify(all_prcp_scores)

@app.route("/api/v1.0/stations")
def func_stations():
    """Return a list of all stations"""
    # Query all stations
    station_results = session.query(Station.station).all()

    # Convert into normal list using np.ravel
    all_stations = list(np.ravel(station_results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a dictionary of last twelves months of temperature observations."""
    # Query all precipitation scoress.
    tobs_data_results=session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date>'2016-08-23').filter(Measurement.date<'2017-08-24').\
    order_by(Measurement.date.desc()).all()

    # Create a dictionary from the row data and append to a list of all temperature values
    all_tobs = []
    for tobs_values in tobs_data_results:
        tobs_dict = {"date" : tobs_values.date, "tobs" : tobs_values.tobs}
        all_tobs.append(tobs_dict)

    # Return json representation of dictionary                 
    return jsonify(all_tobs)


@app.route("/api/v1.0/start_date/<start_date1>")
def temp_stats1(start_date1):
    """Return TMIN, TAVG, and TMAX for all dates greater than or equal to <start_date>."""
    # Query to calculate and return temp stats given start date only.
    sel1 = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    temp_stats_results=session.query(*sel1).filter(Measurement.date>=start_date1).all()

    # Unpact query list
    temp_stats_sdate = list(np.ravel(temp_stats_results))

    # Return json representation of dictionary                 
    return jsonify(temp_stats_sdate)  



@app.route("/api/v1.0/<start>/<end>")
def temp_stats2(start,end):
    """Return TMIN, TAVG, and TMAX for all dates greater than or equal to <start_date>."""
    # Query to calculate and return temp stats given start date only.
    sel2 = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    temp_stats_results2=session.query(*sel2).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    print(temp_stats_results2)

    # Unpact query list
    temp_stats_sdate2 = list(np.ravel(temp_stats_results2))

    # Return json representation of dictionary                 
    return jsonify(temp_stats_sdate2)  


if __name__ == "__main__":
    app.run(debug=True)
