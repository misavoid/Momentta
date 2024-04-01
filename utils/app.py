# app.py

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import plotly.express as px
import pandas as pd

# Initialization
app = Flask(__name__, template_folder='utils/templates')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///momentta_tracking.db"
db = SQLAlchemy(app)


# Define your data model
class Usage(db.Model):
    __tablename__ = "usage"

    id = db.Column(db.Integer, primary_key=True)
    app = db.Column(db.String)
    time_spent = db.Column(db.Integer)


@app.route("/")
def dashboard():
    # Query data from Sqlite
    data = Usage.query.all()
    df = pd.DataFrame([datum.__dict__ for datum in data])

    # Create visualizations
    fig_usage = px.bar(df, x='app', y='time_spent')
    fig_usage_div = fig_usage.to_html(full_html=False)

    return render_template('dashboard.html', fig_usage_div=fig_usage_div)
