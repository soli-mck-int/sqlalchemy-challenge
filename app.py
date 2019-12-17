import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine,func
import datetime as dt
import numpy as np
from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")
Base=automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app=Flask(__name__)

@app.route('/')
def home():
    return (
        f"Welcome to the Surf Vocation API!<br/><br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route('/api/v1.0/precipitation')
def prps():
    session=Session(engine)
    query_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    recent = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date>=query_date).all()
    prcp_info=[]
    for date,prcp in recent:
        dicts={}
        dicts['date']=date
        dicts['prcp']=prcp
        prcp_info.append(dicts)
    return jsonify(prcp_info)

@app.route('/api/v1.0/stations')
def route2():
    session=Session(engine)
    result=session.query(Station.name,Station.station,Station.elevation).all()
    station=[]
    for row in result:
        re={}
        re['name']=row[0]
        re['station']=row[1]
        re['elevation']=row[2]
        station.append(re)
    return jsonify(station)

@app.route('/api/v1.0/tobs')
def route3():
    session=Session(engine)
    begin_date = dt.date(2017,1,1)
    end_date=dt.date(2018,1,1)
    results=session.query(Station.name, Measurement.station, Measurement.tobs).filter(Measurement.date>=begin_date).filter(Measurement.date<=end_date).all()
    temp=[]
    for row in results:
        theresult={}
        theresult['name']=row[0]
        theresult['station']=row[1]
        theresult['tobs']=row[2]
        temp.append(theresult)
    return jsonify(temp)

@app.route('/api/v1.0/<start>')
def route4(start=None):
    session=Session(engine)
    return_re=session.query(Measurement.date,func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date>=start).group_by(
        Measurement.date).all()
    re_four=list(return_re)
    return jsonify(re_four)

@app.route("/api/v1.0/<start>/<end>")
def route5(start=None,end=None):
    duration = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs),
                               func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).group_by(
        Measurement.date).all()
    refive=list(duration)
    return jsonify(refive)    



if __name__ == "__main__":
    app.run(debug=True)