import threading
import sqlite3
import time
import tkinter as tk
from os import wait4

from tenacity import sleep

from utils.load_categories import load_configurations
from utils.flask_app.app import app
from utils.capture_momentt import ActivityTracker
import logging

database = "dbs/momentta_categories.db"



def run_flask():
    app.run(debug=True, use_reloader=False)

def run_momentta():
    # Load configurations from database
    rules = load_configurations(database)

    print("Loaded rules: ", rules)  # Debug output

    # Create ActivityTracker instance
    tracker = ActivityTracker(db_path='dbs/momentta_tracking.db', category_rules=rules)

    print("ActivityTracker created, starting tracking...")

    while True:
        try:
            tracker.start_tracking()
        except Exception as e:
            print(f"An error occurred: {e}")
            print('retrying in five seconds...')
            time.sleep(5)


if __name__ == "__main__":

    # Start the Momentta tracking in a separate thread
    tracking_thread = threading.Thread(target=run_momentta)
    tracking_thread.start()

    # Start the Flask app in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Join the threads to keep the main thread alive
    tracking_thread.join()
    flask_thread.join()