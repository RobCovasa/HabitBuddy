
# HabitBuddy: Your Companion for Habit Formation

HabitBuddy is a user-friendly, simple-to-use application designed to assist individuals in developing and sustaining healthy behaviors. It aims to streamline and enliven the processes of habit creation, management, and tracking.

## 🎯 Features

-   🛠 **Create, Edit, and Delete Habits:** Personalize your habits list to your heart's content.
-   ✅ **Mark Habits as Complete:** Celebrate every accomplishment, no matter how small.
-   🔥 **Calculate Current Streak for Habits:** Keep your motivation high with visible progress.
-   🔍 **Filter Habits by Periodicity:** Organize your habits into daily or weekly schedules.
-   📊 **Generate a Summary Report of All Habits:** Review your progress at a glance.
-   💯 **Calculate Completion Rates for All Habits:** See how often you're hitting your goals.

## ⚙️ Dependencies

-   Python 3.6 or later
-   Fire (Command-line interface)
-   Colorama (Colored terminal output)
-   ipython (For Fire)

## 📥 Installation

1.  Clone the repository

bashCopy code

`https://github.com/RobCovasa/HabitBuddy.git` 

2.  Install the required packages

bashCopy code

`cd HabitBuddy
pip install -r requirements.txt` 

## 📘 Basic Usage

### 🚀 Starting the Application

-   Open your terminal.
-   Navigate to the directory containing the `main.py` file.
-   Run the `main.py` file by typing `python main.py` into the terminal and pressing Enter.

### 🆕 Creating a New Habit

-   Run the following command:

bashCopy code

`python main.py create <name> <description> <start_date> <periodicity>` 

-   For example:

bashCopy code

`python main.py create "Drink 8 glasses of water" "Drink 8 glasses of water per day" 2023-01-01 daily` 

### ✏️ Editing a Habit

-   Run the following command:

bashCopy code

`python main.py edit <habit_name> [--name <new_name>] [--description <new_description>] [--start_date <new_start_date>] [--periodicity <new_periodicity>]` 

-   For example:

bashCopy code

`python main.py edit "Drink 8 glasses of water" --name "Drink 10 glasses of water" --description "Drink 10 glasses of water per day" --start_date 2023-02-01` 

### 🗑️ Deleting a Habit

-   Run the following command:

bashCopy code

`python main.py delete <habit_name1> [<habit_name2> ...]` 

-   For example:

bashCopy code

`python main.py delete "Drink 8 glasses of water" "Go for a 30-minute walk"` 

### 📈 Tracking Streaks

-   To calculate and view the **current streak** for a specific habit, use the `streak` command:

bashCopy code

`python main.py streak <habit_name>` 

markdownCopy code

``- For example: `python main.py streak "Drink 8 glasses of water"` `` 

-   To calculate and view the **longest streak** for a specific habit, use the `longest_streak` command:

bashCopy code

`python main.py longest_streak <habit_name>` 

markdownCopy code

``- For example: `python main.py longest_streak "Drink 8 glasses of water"` `` 

-   To calculate and view the **longest streak for all habits**, use the `longest_streak_all` command:

bashCopy code

`python main.py longest_streak_all` 

### 👀 Viewing All Habits

-   To view all your habits, use the following command:

bashCopy code

`python main.py all_habits` 

### 🔍 Filtering Habits

-   To filter habits by periodicity, use the `filter` command:

bashCopy code

`python main.py filter <periodicity>` 

markdownCopy code

``- For example: `python main.py filter daily` `` 

### 💯 Viewing Completion Rates

-   To view the completion rates of your habits, use the `completion_rates` command:

bashCopy code

`python main.py completion_rates` 

### ✅ Marking a Habit as Complete

-   To mark a habit as complete, use the `complete` command:

bashCopy code

`python main.py complete <habit_name> [--completion_datetime <completion_datetime>]` 

luaCopy code

``- For example: `python main.py complete "Drink 8 glasses of water" --completion_d``