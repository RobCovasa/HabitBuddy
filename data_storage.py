import json
from habit_manager import Habit
from colorama import Fore, Style

def load_info(file_path):
    '''Load data from a JSON file and return a list of habits'''
    print(f"{Fore.YELLOW}{Style.BRIGHT}Loading data from file: {file_path}{Style.RESET_ALL}")
    # try and except to catch errors
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            habit_list = [Habit.from_dictionary(habit_dict) for habit_dict in data["habits"]]
            print(f"{Fore.GREEN}Data loaded successfully{Style.RESET_ALL}")
            return habit_list
    except (FileNotFoundError, json.JSONDecodeError): # FileNotFoundError to catch if file doesn't exist, JSONDecodeError to catch if file is empty
        print(f"{Fore.RED}File not found or empty{Style.RESET_ALL}")
        return []

def save_info(habit_list, file_path):
    '''Save data to a JSON file'''
    print(f"{Fore.GREEN}Saving data to file: {file_path}{Style.RESET_ALL}")
    data = {"habits": [habit.to_dictionary() for habit in habit_list]}
    # try and except to catch errors
    try:
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4) # Indent to make the file more readable
            print(f"{Fore.GREEN}Data saved successfully{Style.RESET_ALL}")
    except IOError: # IOError to catch if file is read-only
        print(f"{Fore.RED}Error saving data{Style.RESET_ALL}")
