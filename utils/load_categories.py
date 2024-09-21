import sqlite3
import logging

def load_configurations(database):
    print("loading configs")
    conn = sqlite3.connect(database)
    curs = conn.cursor()

    category_tables = ["Browsing", "Communication", "Design", "Development", "Entertainment", "Productivity", "SocialMedia",
                       "Utilities"]

    category_rules = {}

    try:
        for table in category_tables:
            # Ensure table exists before querying it
            curs.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            if curs.fetchone() is None:
                logging.warning(f"Table {table} does not exist in the database.")
                continue

            print("loading applications from {table}")
            curs.execute(f"SELECT Application FROM {table}")
            apps = curs.fetchall()
            for app in apps:
                print(app)
                app_name = app[0] if app and app[0] else ''  # Check for valid application names
                print(app_name)
                if app_name:
                    category_rules[app_name.lower()] = table
                    print(f"mapped '{app_name.lower()}' to category '{table}'")
    except sqlite3.Error as e:
        logging.error(f"Database error occurred: {e}")
    finally:
        curs.close()
        conn.close()

    return category_rules

class CategoryMapper:
    def __init__(self, database):
        print("Initializing CategoryMapper...")
        self.category_rules = load_configurations(database)
        print(f"Category rules loaded: {len(self.category_rules)} entries")

    def map_app_to_category(self, app):
        normalized_app = app.lower()
        print(f"Mapping application '{app}' (normalized: '{normalized_app}') to category...")

        if normalized_app in self.category_rules:
            category = self.category_rules[normalized_app]
            print(f"Application '{app}' successfully mapped to category '{category}'")
        else:
            category = "Uncategorized"
            print(f"Application '{app}' not found in category rules, mapped to 'Uncategorized'")

        return category
