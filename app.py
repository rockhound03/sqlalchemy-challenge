from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
import os
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc
#from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#C:\Users\jason\Documents\GitHub\sqlalchemy-challenge\Resources
path_too = os.path.join("sqlite:///", "Resources/", "hawaii.sqlite")
#path =  os.path.join("sqlite:///." + os.getcwd(), "sqlalchemy-challenge\\Resources\\hawaii.sqlite")
db_path =  os.path.join("Resources", "hawaii.sqlite")
con_string = f"sqlite:///{db_path}"
absolute_path = "sqlite:///C:\\Users\\jason\\Documents\\GitHub\\sqlalchemy-challenge\\Resources\\hawaii.sqlite"
engine = create_engine(con_string)
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

def GetLastYear():
    lstdate = session.query(Measurement.date).all()
    session.close()
    i = len(lstdate)
    testdate = lstdate[i-1][0]
    dateout = dt.datetime.strptime(testdate,'%Y-%m-%d')
    oneyear = dateout - dt.timedelta(days=366)
    return oneyear

@app.route("/")
def welcome():
    return (
        f"Welcome to the Weather API!<br/>"
        f"---------------------------<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/stations<br/>"
        f"Returns list of stations."
        f"---------------------------<br/>"
        f"/api/v1.0/tobs<br/>"
        f"Returns temperature data for last year of database.<br/>"
        f"---------------------------<br/>"
        f"/api/v1.0/start_date<br/>"
        f"start_date :: returns min, max and avg temperature for start date to last date of db.<br/>"
        f"---------------------------<br/>"
        f"/api/v1.0/start_date/end_date<br/>"
        f"start_date / end_date :: returns min, max and avg temperature for start date to end date of db.<br/>"
        
    )

@app.route("/api/v1.0/stations")
def stations():
    station_list = []
    stations = session.query(Measurement.station).distinct()
    session.close()
    for station in stations:
        station_list.append({"station_id" : station[0]})
    
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    #query for the dates and temperature observations from a year from the last data point.
    #Return a JSON list of Temperature Observations (tobs) for the previous year.
    last_year_list = []
    #search_year = GetLastYear
    lstdate = session.query(Measurement.date).all()
    session.close()
    i = len(lstdate)
    testdate = lstdate[i-1][0]
    dateout = dt.datetime.strptime(testdate,'%Y-%m-%d')
    oneyear = dateout - dt.timedelta(days=366)
    last_year_tobs = session.query(Measurement.date,Measurement.tobs).\
    filter(Measurement.date > oneyear).\
    order_by(Measurement.date).all()
    session.close()
    for measured in last_year_tobs:
        last_year_list.append({"date" : measured[0],"tobs" : measured[1]})
    
    return jsonify(last_year_list)

@app.route("/api/v1.0/precipitation")
def precipitation():
    last_year_list = []
    lstdate = session.query(Measurement.date).all()
    i = len(lstdate)
    testdate = lstdate[i-1][0]
    dateout = dt.datetime.strptime(testdate,'%Y-%m-%d')
    oneyear = dateout - dt.timedelta(days=366)
    last_year_prcp = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > oneyear).\
    order_by(Measurement.date).all()
    session.close()
    for measured in last_year_prcp:
        last_year_list.append({measured[0] : measured[1]})
    return jsonify(last_year_list)

@app.route("/api/v1.0/<start_date>")
def start(start_date):
    stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start_date).all()
    session.close()
    temp_stats = [{"tmin" : stats[0][0], "tavg" : np.around(stats[0][1],1), "tmax" : stats[0][2]}]
    return jsonify(temp_stats)

@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end(start_date, end_date):
    stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    session.close()
    temp_stats = [{"tmin" : stats[0][0], "tavg" : np.around(stats[0][1],1), "tmax" : stats[0][2]}]
    return jsonify(temp_stats)

if __name__ == "__main__":
    app.run(debug=True,port=5006)
