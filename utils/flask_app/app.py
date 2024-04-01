from flask import Flask, jsonify, render_template
import sqlite3


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

    # Convert the records to a list of dictionaries
    records_list = [dict(zip(['timestamp', 'window_title', 'application', 'category'], record)) for record in records]

    return render_template('dashboard.html', records=records_list)

