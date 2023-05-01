import json
from habit_manager import Habit

def load_info(file_path):
    '''Load data from a JSON file and return a list of habits'''
    with open(file_path, "r") as file:
        data = json.load(file)
        habit_list = [Habit.from_dictionary(habit_dict) for habit_dict in data["habits"]]
        return habit_list

def save_info(habit_list, file_path):
    '''Save data to a JSON file'''
    data = {"habits": [habit.to_dictionary() for habit in habit_list]}
    with open(file_path, "w") as file:
        json.dump(data, file)