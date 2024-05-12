from flask import Flask, jsonify, render_template
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.io as pio
app = Flask(__name__)


@app.route('/')
def home():
    return "Hello, this is a minimalistic Flask application!"


@app.route('/dashboard')
def dashboard():
    # Connect to the SQLite database
    connection = sqlite3.connect('momentta_tracking.db')
    cursor = connection.cursor()

    # Execute a SQL query to fetch all records from the activity_log table
    cursor.execute('SELECT * FROM activity_log')
    records = cursor.fetchall()

    # Close the connection to the database
    connection.close()

    # Convert the records to a pandas DataFrame
    df = pd.DataFrame(records, columns=['timestamp', 'window_title', 'application', 'category'])

    # Create a bar chart with Plotly
    fig = px.bar(df, x='category', y='timestamp', title='Number of activities per category')

    # Convert the figures to HTML div string
    graph_div = pio.to_html(fig, full_html=False)

    # Convert the records to a list of dictionaries
    records_list = df.to_dict('records')

    return render_template('dashboard.html', records=records_list, graph_div=graph_div)

