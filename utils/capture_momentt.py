import sqlite3
import psutil
import time
from datetime import datetime
from typing import Optional, Tuple
from utils.identifiers.getWindowTitle import get_active_window_title
from utils.identifiers.getApplicationTitle import get_active_application


# TODO: outsource the category rules to different file
# TODO: find out how to automatically create the database and start it from the main.py


class ActivityTracker:
    def __init__(self, db_path: str, category_rules: dict):
        self.db_path = db_path
        self.afk_threshold = 30  # seconds
        self.last_activity_time = time.time()
        self.category_rules = category_rules
        self.current_activity = None
        self.start_time = None

        # Initialize the database
        self.initialize_database()

    def initialize_database(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activity_log (
                timestamp TEXT,
                window_title TEXT,
                application TEXT,
                category TEXT,
                duration REAL
            )
        ''')
        connection.commit()
        connection.close()

    def map_app_to_category(self, app):
        app_lower = app.lower()
        for app_name, category in self.category_rules.items():
            if app_name.lower() == app_lower:
                return category
        return "Uncategorized"

#TODO: i have no idea why the category mapping isn't working. suspected a problem with upper and lowercase handling but either im missing something or that's not the problem

    def capture_moment(self):
        window_title = get_active_window_title()
        app = get_active_application()

        if app:
            category = self.map_app_to_category(app)  # map based on the application title

            if self.current_activity and app != self.current_activity:
                # Calculate duration of the previous activity
                end_time = datetime.now()
                duration = (end_time - self.start_time).total_seconds()
                # Log the previous activity
                self.log_activity(self.current_activity['window_title'],
                                  self.current_activity['app'],
                                  self.current_activity['category'],
                                  duration)

            # Start tracking the new activity
            self.current_activity = {'window_title': window_title, 'app': app, 'category': category}
            self.start_time = datetime.now()

            # Update the last activity time
            self.last_activity_time = time.time()

#TODO: fix afk feature

        elif time.time() - self.last_activity_time > self.afk_threshold:
            self.log_activity('AFK', 'AFK', 'AFK', 0)
            self.current_activity = None


            '''self.log_activity(window_title, app, category)  # log both window and app titles
            self.last_activity_time = time.time()

        elif time.time() - self.last_activity_time > self.afk_threshold:
            self.log_activity('AFK', 'AFK', 'AFK')'''

    def log_activity(self, window_title: str, app: str, category: str, duration: float):
        timestamp = datetime.now().isoformat()
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO activity_log (timestamp, window_title, application, category, duration) 
            VALUES (?, ?, ?, ?, ?)
        ''', (timestamp, window_title, app, category, duration))
        connection.commit()
        connection.close()

    def start_tracking(self, interval: int = 5):
        # You can decide the interval in seconds
        while True:
            app = get_active_application()
            category = self.map_app_to_category(app)
            self.capture_moment()
            print(f"Activity captured: {get_active_window_title()} + {category}")
            print("Activity logged.")
            time.sleep(interval)
