import json
from habit_manager import Habit
from colorama import Fore, Style

def load_info(file_path):
    '''Function to load data from a JSON file.'''
    print(f"{Fore.YELLOW}{Style.BRIGHT}Loading data from file: {file_path}{Style.RESET_ALL}")
    # Catch and handle any errors that may occur during file operations
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            # Convert each dictionary in data["habits"] into a Habit object using Habit.from_dictionary
            habit_list = [Habit.from_dictionary(habit_dict) for habit_dict in data["habits"]]
            print(f"{Fore.GREEN}Data loaded successfully{Style.RESET_ALL}")
            return habit_list
    # Catch FileNotFoundError if the file does not exist and JSONDecodeError if the file content is not valid JSON
    except (FileNotFoundError, json.JSONDecodeError): 
        print(f"{Fore.RED}Error: {Style.RESET_ALL} File not found or empty")
        return [] # Return an empty list if an error occurred

def save_info(habit_list, file_path):
    '''Function to save data to a JSON file.'''
    print(f"{Fore.GREEN}Saving data to file: {file_path}{Style.RESET_ALL}")
    # Convert each Habit object in habit_list to a dictionary using Habit.to_dictionary
    data = {"habits": [habit.to_dictionary() for habit in habit_list]}
    # Catch and handle any errors that may occur during file operations
    try:
        with open(file_path, "w") as file:
            # Use json.dump to write data to the file, indenting it for readability
            json.dump(data, file, indent=4) 
            print(f"{Fore.GREEN}Data saved successfully{Style.RESET_ALL}")
    # Catch IOError
    except IOError: 
        print(f"{Fore.RED}Error: {Style.RESET_ALL} Saving data failed")