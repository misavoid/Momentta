import threading
import sqlite3
from utils.flask_app.app import app
from utils.capture_momentt import ActivityTracker

database = "momentta_categories.db"


def load_configurations(database):
    conn = sqlite3.connect(database)
    curs = conn.cursor()

    category_tables = ["Communication", "Design", "Development", "Entertainment", "Productivity", "SocialMedia",
                       "Utilities"]

    category_rules = {}
    for table in category_tables:
        curs.execute(f"SELECT Application FROM {table}")
        apps = curs.fetchall()
        category = table.lower()
        for app in apps:
            app_name = app[0].lower() if app[0] else ''
            category_rules[app_name] = category

    curs.close()
    conn.close()

    return category_rules


def main():
    # Load configurations from database
    rules = load_configurations(database)

    print("Loaded rules: ", rules)  # Debug output

    # Create ActivityTracker instance
    tracker = ActivityTracker(db_path='momentta_tracking.db', category_rules=rules)

    print("ActivityTracker created, starting tracking...")

    # Make sure the SQLite database exists and all tables are created

    try:
        tracker.start_tracking()
    except Exception as e:
        print(f"An error occurred: {e}")


def run_flask():
    app.run(debug=True, use_reloader=False)


if __name__ == "__main__":
    # Start the Flask app in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    main()
# %%
