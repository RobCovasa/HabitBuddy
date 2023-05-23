import json
from habit_manager import Habit
from colorama import Fore, Style

def load_info(file_path):
    '''Load data from the JSON file.'''
    print(f"{Fore.YELLOW}{Style.BRIGHT}Loading data from file: {file_path}{Style.RESET_ALL}")
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            habit_list = [Habit.from_dictionary(habit_dict) for habit_dict in data["habits"]]
            print(f"{Fore.GREEN}Data loaded successfully{Style.RESET_ALL}")
            return habit_list
    except (FileNotFoundError, json.JSONDecodeError): 
        print(f"{Fore.RED}Error: {Style.RESET_ALL} File not found or empty")
        return []

def save_info(habit_list, file_path):
    '''Save data to the JSON file.'''
    print(f"{Fore.GREEN}Saving data to file: {file_path}{Style.RESET_ALL}")
    data = {"habits": [habit.to_dictionary() for habit in habit_list]}
    try:
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4) 
            print(f"{Fore.GREEN}Data saved successfully{Style.RESET_ALL}")
    except IOError: 
        print(f"{Fore.RED}Error: {Style.RESET_ALL} Saving data failed")