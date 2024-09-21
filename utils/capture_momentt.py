import sqlite3
import psutil
import time
from datetime import datetime
from utils.load_categories import CategoryMapper
from utils.identifiers.getWindowTitle import get_active_window_title
from utils.identifiers.getApplicationTitle import get_active_application

class ActivityTracker:
    def __init__(self, db_path: str, category_rules: dict):
        self.db_path = db_path
        self.afk_threshold = 30  # seconds
        self.last_activity_time = time.time()
        self.category_rules = category_rules
        self.current_activity = None
        self.start_time = None
        # Initialize CategoryMapper once
        self.category_mapper = CategoryMapper(database='dbs/momentta_categories.db')
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

    def capture_moment(self):
        try:
            window_title = get_active_window_title() or 'Unknown Window'
            app = get_active_application() or 'Unknown Application'

            # Normalize application name (lowercase)
            app_normalized = app.lower()

            # Use the category mapper
            category = self.category_mapper.map_app_to_category(app_normalized)

            if self.current_activity is None:
                self.current_activity = {'window_title': window_title, 'app': app, 'category': category}
                self.start_time = datetime.now()
                self.last_activity_time = time.time()
                return

            # Check if the application changed or user went AFK
            if app != self.current_activity['app'] or time.time() - self.last_activity_time > self.afk_threshold:
                end_time = datetime.now()
                duration = (end_time - self.start_time).total_seconds()

                self.log_activity(self.current_activity['window_title'],
                                  self.current_activity['app'],
                                  self.current_activity['category'],
                                  duration)

                self.current_activity = {'window_title': window_title, 'app': app, 'category': category}
                self.start_time = datetime.now()
                self.last_activity_time = time.time()

            elif time.time() - self.last_activity_time > self.afk_threshold:
                self.log_activity('AFK', 'AFK', 'AFK', 0)
                self.current_activity = 'afk'

        except Exception as e:
            print(f"An error occurred during activity capture: {e}")

    def log_activity(self, window_title: str, app: str, category: str, duration: float):
        try:
            timestamp = datetime.now().isoformat()
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute('''
                INSERT INTO activity_log (timestamp, window_title, application, category, duration) 
                VALUES (?, ?, ?, ?, ?)
            ''', (timestamp, window_title, app, category, duration))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Database error occurred: {e}")
        finally:
            connection.close()


    def start_tracking(self, interval: int = 5):
        # Track activity at the defined interval
        while True:
            self.capture_moment()
            if self.current_activity and isinstance(self.current_activity, dict):
                print(f"Activity captured: {self.current_activity['window_title']} + {self.current_activity['category']}")
            print("Activity logged.")
            time.sleep(interval)

