import sqlite3
import logging

def load_configurations(database):
    conn = sqlite3.connect(database)
    curs = conn.cursor()

    category_tables = ["Communication", "Design", "Development", "Entertainment", "Productivity", "SocialMedia",
                       "Utilities"]

    category_rules = {}
    for table in category_tables:
        curs.execute(f"SELECT Application FROM {table}")
        apps = curs.fetchall()
        if table is not None:
            category = table
        else:
            category = ''
            logging.warning(f"Table name is None, setting category to empty string.")
        for app in apps:
            app_name = app[0] if app[0] is not None else ''
            category_rules[app_name] = category

    curs.close()
    conn.close()

    return category_rules

class CategoryMapper:
    def __init__(self, database):
        self.category_rules = load_configurations(database)

    def map_app_to_category(self, app):
        for tracked_app, category in self.category_rules.items():
            if app == tracked_app:
                return category
        return "Uncategorized"

