import sqlite3
from utils.app import app
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
    rules = load_configurations(database)
    print("Loaded rules: ", rules)  # Debug output
    tracker = ActivityTracker(db_path='momentta_tracking.db', category_rules=rules)

    print("ActivityTracker created, starting tracking...")

    try:
        tracker.start_tracking()
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
    app.run(debug=True)

# %%
