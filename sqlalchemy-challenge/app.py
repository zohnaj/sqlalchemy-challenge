#!/usr/bin/env python
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine=create_engine("sqlite:///hawaii.sqlite")
Base=automap_base()
Base.prepare(engine, reflect=True)

Measurement=Base.classes.measurement
Station=Base.classes.station

session=Session(engine)
app=Flask(__name__)


@app.route("/")
def home_page():
    return(
        f"Welcome to the Home Page<br/>"
        f"Available Routes: <br/>"
    
        f"/api/v1.0/precipitation<br/>"
        f"Returns dates and precipitation from last year<br/>"

        f"/api/v1.0/stations<br/>"
        f"Returns list of stations<br/>"

        f"/api/v1.0/tobs<br/>"
        f"Returns dated and observed temperatures for the last year<br/>"

        f"/api/v1.0/<start>/api/v1.0/<start>/<end<br/>"
        f"Returns list of the min, avg, and max temperatures for given date range<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Returns dates and precipitation from last year"""
    final_results=session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= '2016-08-23').filter(Measurement.date <='2017-08-23').all()

    prcp_results=[]
    for final_result in final_results:
        prcp_dict={}
        prcp_dict['date']=final_result[0]
        prcp_dict['prcp']=final_result[1]
        prcp_results.append(prcp_dict) 
    return jsonify(prcp_results)

@app.route("/api/v1.0/stations")
def stations():
    """Returns station list"""
    stations_results=session.query(Station.name).all()
    stations=pd.read_sql(stations_results, Station.name.session.bind)

    all_stations=list(np.ravel(stations))
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Returns observed temperatures for #most active in the last year"""
    temp_results=session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= '2016-08-23').filter(Measurement.date <='2017-08-23').all()
    
    tobs_results=[]
    for temp_result in temp_results:
        tobs_dict={}
        tobs_dict["date"]=temp_result[0]
        tobs_dict["tobs"]=temp_result[1]
        tobs_results.append(tobs_dict)
    return jsonify(tobs_results)

@app.route("/api/v1.0/<start>")
def start_date(start,end):
    start=2016-8-23
    end=start-365
    """Returns list of the min, avg, and max temperatures for given date range"""
    results=session.query(func.min(Measurement.tobs).\
    func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date)
    
    data_results_start_end=list(np.ravel(results))
    return jsonify(data_results_start_end)

@app.route("/api/v1.0/<start>/<end>")
def date_range(start1,end1):
    start1=2016-8-23
    end1=2017-8-23
    """Returns list of the min, avg, and max temperatures for given date range"""
    results=session.query(func.min(Measurement.tobs).\
    func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date)
    
    data_results_start_end=list(np.ravel(results))
    return jsonify(data_results_start_end)

if __name__=='__main__':
    app.debug=True
    app.run