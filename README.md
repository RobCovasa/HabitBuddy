# HabitBuddy
The HabitBuddy App is a user-friendly and simple-to-use program created to help people develop and maintain healthy behaviors. The main goals of the app are to simplify and make habit creation, management, and tracking enjoyable for users.

## Features
* Create, edit, and delete habits
* Mark habits as complete
* Calculate current streak for habits
* Filter habits by periodicity (daily or weekly)
* Generate a summary report of all habits
* Calculate completion rates for all habits

## Dependencies
* Python 3.6 or later
* Fire for the command-line interface
* Colorama for colored terminal output

## Installation
* Clone the repository
```
https://github.com/RobCovasa/HabitBuddy.git
```
* Install the required packages
```
cd HabitBuddy
pip install -r requirements.txt
```

# Basic Usage
## Starting the Application
- Open your terminal.
- Navigate to the directory containing the main.py file.
- Run the main.py file by typing python main.py into the terminal and pressing Enter.

## Creating a New Habit
- Type python main.py create <name> <description> <start_date> <periodicity> into the terminal.
- For example: python main.py create "Drink 8 glasses of water" "Drink 8 glasses of water per day" 2023-01-01 daily

## Editing a Habit
- Type python main.py edit <habit_name> [--name <new_name>] [--description <new_description>] [--start_date <new_start_date>] [--periodicity <new_periodicity>] into the terminal.
- For example: python main.py edit "Drink 8 glasses of water" --name "Drink 10 glasses of water" --description "Drink 10 glasses of water per day" --start_date 2023-02-01

## Deleting a Habit
- Type python main.py delete <habit_name1> [<habit_name2> ...] into the terminal.
- For example: python main.py delete "Drink 8 glasses of water" "Go for a 30-minute walk"

## Tracking Streaks
#### To calculate and view the current streak for a specific habit, use the streak command:
- Type python main.py streak <habit_name> into the terminal.
- For example: python main.py streak "Drink 8 glasses of water"

#### To calculate and view the longest streak for a specific habit, use the longest_streak command:
- Type python main.py longest_streak <habit_name> into the terminal.
- For example: python main.py longest_streak "Drink 8 glasses of water"

#### To calculate and view the longest streak for all habits, use the longest_streak_all command:
- Type python main.py longest_streak_all into the terminal.

## Viewing All Habits
- Type python main.py all_habits

## Filtering Habits
- Type python main.py filter <periodicity> into the terminal.
- For example: python main.py filter daily

## Viewing Completion Rates
- Type python main.py completion_rates into the terminal.

## Marking a Habit as Complete
- Type python main.py complete <habit_name> [--completion_datetime <completion_datetime>]
- For example: python main.py complete "Drink 8 glasses of water" --completion_datetime 2023-01-01T12:00:00