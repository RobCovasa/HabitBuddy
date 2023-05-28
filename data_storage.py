import json
from habit_manager import Habit
from colorama import Fore, Style

def load_info(file_path):
    '''
    Load habit data from a JSON file.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        list: List of Habit objects.
    '''
    print(f'{Fore.YELLOW}{Style.BRIGHT}Loading data from file: {file_path}{Style.RESET_ALL}')
    
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            habit_list = [Habit.from_dictionary(habit_dict) for habit_dict in data['habits']] # Create a Habit object from each dictionary in the list of dictionaries
            
            print(f'{Fore.GREEN}Data loaded successfully{Style.RESET_ALL}')
            return habit_list
    except (FileNotFoundError, json.JSONDecodeError): 
        print(f'{Fore.RED}Error: {Style.RESET_ALL} File not found or failed to decode JSON data.')
        return []


def save_info(habit_list, file_path):
    '''
    Save habit data to a JSON file.

    Args:
        habit_list (list): List of Habit objects.
        file_path (str): Path to the JSON file where data will be saved.
    '''
    print(f'{Fore.GREEN}Saving data to file: {file_path}{Style.RESET_ALL}')

    data = {'habits': [habit.to_dictionary() for habit in habit_list]}
    
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4) # Indent the data for readability
            
            print(f'{Fore.GREEN}Data saved successfully{Style.RESET_ALL}')
    except IOError:
        print(f'{Fore.RED}Error: {Style.RESET_ALL} Failed to save data.')