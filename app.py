import numpy as np
import pandas as pd
import datetime as dt

import sqlachemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func

from flask import Flask, jsonif
  
###########################################
#Database Setup
###########################################

engine = create_engine(\"sqlite:///Resources/hawaii.sqlite\")
   
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

app = Flask(_name_)


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
    prcp_data_results=session.query(Measurement.date, func.sum(Measurement.prcp)).\
    filter(Measurement.date>'2016-08-23').filter(Measurement.date<'2017-08-24').\
    order_by(Measurement.date.desc()).all()

    # Create a dictionary from the row data and append to a list of all precipitation scores
    all_prcp_scores = []
    for prcp_score in prcp_data_results:
        prcp_dict = {"date" : prcp}
        all_prcp_scores.append(prcp_dict)

    # Return json representation of dictionary                 
    return jsonify(all_prcp_scores)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all stations"""
    # Query all stations
    station_results = session.query(Station.name).all()

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
        tobs_dict = {"date" : tobs}
        all_tobs.append(tobs_dict)

    # Return json representation of dictionary                 
    return jsonify(all_tobs)


 @app.route("/api/v1.0/start_date/<start_date>")
def temp_stats():
    """Return TMIN, TAVG, and TMAX for all dates greater than or equal to <start_date>."""
    # Query to calculate and return temp stats given start date only.
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    temp_stats_results=session.query(Measurement.date,*sel).filter(Measurement.date>=start_date).\
        order_by(Measurement.date.desc()).all()

    # Unpact query list
    #temp_stats_sdate = list(np.ravel(temp_stats_results))

    # Create a dictionary from the row data and append to a list of all temperature statistics
    all_temp_stats = []
    for tstats in temp_stats_results:
        (tdate, tmin, tavg, tmax)=tstats
        temp_sdate_dict = {}
        temp_sdate_dict["date"] = tdate
        temp_sdate_dict["min"] = tmin
        temp_sdate_dict["avg"] = tavg
        temp_sdate_dict["max"] = tmax
        all_temp_stats.append(temp_sdate_dict)

    # Return json representation of dictionary                 
    return jsonify(all_temp_stats)  


@app.route("/api/v1.0/start_date/end_date/<start_date>/<end_date>")
def SEdate_temp():
    """Return TMIN, TAVG, and TMAX for dates between start date and end date."""
    # Query to calculate and return temp stats given start date only.
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    SEdate_temp_stats=session.query(Measurement.date,*sel).filter(Measurement.date>=start_date).\
        filter(Measurement.date>=start_date).filter(Measurement.date<=end_date).all()
        order_by(Measurement.date.desc()).all()

    # Unpact query list
    #temp_stats_sdate = list(np.ravel(temp_stats_results))

    # Create a dictionary from the row data and append to a list of all temperature statistics
    all_SEdate_temp = []
    for SEtstats in SEdate_temp_stats:
        (SEdate, SEmin, SEavg, SEmax)=SEtstats
        SEtemp_date_dict={}
        SEtemp_sdate_dict["date"] = SEdate
        SEtemp_sdate_dict["min"] = SEmin
        SEtemp_sdate_dict["avg"] = SEavg
        SEtemp_sdate_dict["max"] = SEmax
        all_SEdate_temp.append(SEtemp_sdate_dict)

    # Return json representation of dictionary                 
    return jsonify(all_SEdate_temp)  

if __name__ == '__main__':
    app.run(debug=True)

