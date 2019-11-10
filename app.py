from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc

app = Flask(__name__)




@app.route("/")
def welcome():
    return (
        f"Welcome to the Weather API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )

if __name__ == "__main__":
    app.run(debug=True,port=5006)
