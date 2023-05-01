import json
from habit_manager import Habit

def load_info(file_path):
    '''Load data from a JSON file and return a list of habits'''
    print(f"Loading data from file: {file_path}")
    # try and except to catch errors
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            habit_list = [Habit.from_dictionary(habit_dict) for habit_dict in data["habits"]]
            print("Data loaded successfully")
            return habit_list
    except (FileNotFoundError, json.JSONDecodeError): # FileNotFoundError to catch if file doesn't exist, JSONDecodeError to catch if file is empty
        print("File not found or empty")
        return []

def save_info(habit_list, file_path):
    '''Save data to a JSON file'''
    print(f"Saving data to file: {file_path}")
    data = {"habits": [habit.to_dictionary() for habit in habit_list]}
    # try and except to catch errors
    try:
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4) # Indent to make the file more readable
            print("Data saved successfully")
    except IOError: # IOError to catch if file is read-only
        print("Error saving data")
