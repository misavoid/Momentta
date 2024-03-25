from utils.capture_momentt import ActivityTracker
import json
import os

category_dir = "utils/categories/"
category_rules = {}


def load_configurations():
    for category_file in os.listdir(category_dir):
        if category_file.endswith('.json'):
            with open(os.path.join(category_dir, category_file), 'r') as file:
                category_rules.update(json.load(file))
                return category_rules


def main():
    rules = load_configurations()
    tracker = ActivityTracker(db_path='momentta_tracking.db', category_rules=rules)

    try:
        tracker.start_tracking()
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()

# %%
