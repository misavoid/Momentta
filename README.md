# Momentta 🕰️

Welcome to **Momentta**! An awesome Python project that keeps you accountable by tracking your activities. 🔍

Think of **Momentta** as your personal activity tracker, working behind the scenes to capture and categorize what you're up to, without you needing to lift a finger! 💻

## What does it do? 🧐

At a high level, Momentta uses a set of rules to identify the categories of different activities you are performing on your machine. These rules are loaded from JSON files located in the utils/categories/ directory.

Once the configuration is loaded, Momentta deploys the `ActivityTracker` class from the `utils.capture_momentt` module and begins tracking your activities.

The `ActivityTracker` class accepts two main parameters:
- `db_path`: where the tracking results will be stored (default is `momentta_tracking.db`)
- `category_rules`: the "rules" (app lists) loaded from the `momentta_categories.db` to categorize activities, in which one category has one table with all applications for that category.

## How to use? ☕

Using Momentta to track your activities is as simple as running `main.py` (at the moment. A complete app is planned.) script! It automatically starts tracking your activities and stores them in `momentta_tracking.db`.

## Friendly Reminder 💡

Momentta uses a database file named `momentta_tracking.db` to store the tracked information. Before running, ensure that you have appropriate permissions to read and write to this database file.

## Disclaimer ⚠️

Momentta will log any error that occurred during the tracking process to a not yet existing logfile. 
The error log will probably be stored in the `logs/` directory with the filename `momentta_error.log`.
~~Don't forget to check your terminal window if tracking isn't working as expected. 🕵️~~

Hope you find Momentta helpful in your everyday routine 😄

## Contributions 🤝

Feel free to check out the code! Contributions to Momentta are very much appreciated. Whether it's feature enhancement, bug fixing, or performance improvements, just fork the repository, make your changes and open a pull request. ✨

Happy tracking! 🚀
```