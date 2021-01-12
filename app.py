# Import Dependencies
import os
import pandas as pd
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func
from flask import Flask, jsonify, render_template
from dotenv import load_dotenv

# Create Instance of Flask App
app = Flask(__name__)

# Load Dot Env
load_dotenv()

# Save Password
password = os.getenv("password")

# Set Connection String
connection_string = f"postgres:{password}@localhost:5432/covid_db"

# Set Engine
engine = create_engine(f'postgresql://{connection_string}')

# Automap Base
Base = automap_base()

# Reflect Tables
Base.prepare(engine, reflect=True)

# Save References to Table
Covid = Base.classes.covid_data

# # Create Session
session = Session(engine)


# Create Home Route
@app.route("/")
# Define Index Function
def index():
    """Returns Homepage"""

    # Render Template
    return render_template("index.html")


# Create Dates Route
@app.route("/dates")
# Define Dates Function
def dates():
    """Returns List of Dates for Dropdown"""

    # Selection Information
    sel = [
        Covid.date
    ]

    # Perform SQL Query
    covid_date = session.query(*sel)\
        .order_by(Covid.date.asc())\
        .distinct()\
        .all()

    # Return Jsonified List
    return jsonify(list(covid_date))


# Create Dictionary Route 
@app.route("/total/<date>")
# Define Total Function
def total(date):
    """Returns Dictionary of Values"""

    # # Create Session
    session = Session(engine)
    # Selection Information
    sel = [
        func.sum(Covid.positive_increase),
        func.sum(Covid.positive),
        func.sum(Covid.death_increase),
        func.sum(Covid.death),
        func.sum(Covid.negative_increase),
        func.sum(Covid.negative)
    ]

    # Perform SQL Query
    covid_total = session.query(*sel)\
        .filter(Covid.date == date)\
        .all()
    
    # Save Empty Dictionary
    data_dict = {}
     
    # Add Each Value to Dictionary
    for datum in covid_total:
        data_dict["positive_increase"] = datum[0]
        data_dict["positive"] = datum[1]
        data_dict["death_increase"] = datum[2]
        data_dict["death"] = datum[3]
        data_dict["negative_increase"] = datum[4]
        data_dict["negative"] = datum[5]

    # Returns Jsonified Dictionary
    return jsonify(data_dict)


# Create Positive Increase Route
@app.route("/positive_increase/<date>")
# Define Positive Increase Function
def positive_increase(date):
    """Returns Positive Increase"""

    # # Create Session
    session = Session(engine)
    # Selection Information
    sel = [
        Covid.positive_increase,
        Covid.full_name,
        Covid.presidential_result
    ]

    # Perform SQL Query
    covid_positive_increase = session.query(*sel)\
        .filter(Covid.date == date)\
        .all()

    # Returns Json
    return jsonify(covid_positive_increase)

# Create Death Increase Route 
@app.route("/death_increase/<date>")
# Define Death Increase Function
def death_increase(date):
    """Returns List of Dates for Dropdown"""

    # Create Session
    session = Session(engine)
    # Selection Information
    sel = [
        Covid.death_increase,
        Covid.full_name,
        Covid.presidential_result
    ]

    # Perform SQL Query
    covid_death_increase = session.query(*sel)\
        .filter(Covid.date == date)\
        .all()

    # Returns Json
    return jsonify(covid_death_increase)


# Create Negative Route
@app.route("/negative")
# Define Index Function
def positive():
    """Renders HTML Page for Negative Cases"""

    # Render Template
    return render_template("negative.html")


# Create Negative Increase Route 
@app.route("/negative_increase/<date>")
# Define Negative Increase Function
def negative_increase(date):
    """Returns Negative Increase"""

    # # Create Session
    session = Session(engine)
    # Selection Information
    sel = [
        Covid.negative_increase,
        Covid.full_name,
        Covid.presidential_result
    ]

    # Perform SQL Query
    covid_negative_increase = session.query(*sel)\
        .filter(Covid.date == date)\
        .all()

    # Returns Json
    return jsonify(covid_negative_increase)

# Create Hospitalized Route
@app.route("/hospitalized")
# Define Hospitalized Function
def hospitalized():
    """Returns Hospitalized"""

    # Render Template
    return render_template("hospitalized.html")

# Create Hospitalized Route
@app.route("/hospitalized/<date>")
# Define Hospitalized Date Function
def hospitalized_date(date):
    """Returns Hospitalized Date"""

    # # Create Session
    session = Session(engine)
    # Selection Information
    sel = [
        Covid.hospitalized_currently,
        Covid.recovered,
        Covid.full_name,
        Covid.presidential_result
    ]

    # Perform SQL Query
    covid_hospitalized = session.query(*sel)\
        .filter(Covid.date == date)\
        .all()

    # Returns Jsonified Dictionary
    return jsonify(covid_hospitalized)


# Create Death Route
@app.route("/death")
# Define Death Function
def death():
    """Returns Death"""

    # Render Template
    return render_template("death.html")

# Create Recovered Route
@app.route("/recovered")
# Define Recovered Function
def recovered():
    """Returns Homepage"""

    # Render Template
    return render_template("recovered.html")




if __name__ == "__main__":
    app.run(debug=True)
