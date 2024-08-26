from datetime import date, datetime

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
    df = pd.DataFrame(records, columns=['timestamp', 'window_title', 'application', 'category', 'duration'])
    df['timestamp'] = pd.to_datetime(df['timestamp'])


    df_resampled = df.resample('D', on='timestamp').sum().reset_index()


    today = datetime.now()

    today_df = df_resampled[df_resampled['timestamp'] == today]

    last_week = datetime.now() - pd.Timedelta(days=7)
    last_week_df = df_resampled[df_resampled['timestamp'] >= last_week]

    first_day_of_month = today.replace(day=1)
    this_month_df = df_resampled[df_resampled['timestamp'] >= first_day_of_month]

# Create a bar chart with Plotly
    fig = px.bar(today_df, x='timestamp', y='duration', color='category',
             title='Stacked Activity Duration Over Time', barmode='stack')
    fig.update_xaxes(type='date', tickformat='%Y-%m-%d')

    fig.update_layout(
        updatemenus=[
            dict(
                buttons=list([
                    dict(
                        args=[{'x': [today_df['timestamp']], 'y': [today_df['duration']],
                               'type': 'bar', 'transforms': [dict(type='filter', target='category')]}],
                        label="Today",
                        method="restyle"
                    ),
                    dict(
                        args=[{'x': [last_week_df['timestamp']], 'y': [last_week_df['duration']],
                               'type': 'bar', 'transforms': [dict(type='filter', target='category')]}],
                        label="Last 7 Days",
                        method="restyle"
                    ),
                    dict(
                        args=[{'x': [this_month_df['timestamp']], 'y': [this_month_df['duration']],
                               'type': 'bar', 'transforms': [dict(type='filter', target='category')]}],
                        label="Last 30 Days",
                        method="restyle"
                    )
                ]),
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.1,
                xanchor="left",
                y=1.1,
                yanchor="top"
            ),
        ]
    )

    fig.show()

    # Convert the figures to HTML div string
    graph_div = pio.to_html(fig, full_html=False)

    # Convert the records to a list of dictionaries
    records_list = df.to_dict('records')

    return render_template('dashboard.html', records=records_list, graph_div=graph_div)

