import fire
from colorama import Fore, Style
from datetime import datetime
from habit_manager import create_habit, edit_habit, delete_habit, get_habit_by_name
from analytics import streak_calc, habits_filter, calculate_completion_rates, get_all_habits, calculate_longest_streak, longest_streak_all_habits
from data_storage import load_info, save_info

class HabitTrackerCLI:
    def __init__(self, file_path='habits.json'):
        '''
        Initialize HabitTrackerCLI object.
        Args:
            file_path (str): Path to the habit storage file.
        '''
        self.file_path = file_path
        self.habit_list = load_info(file_path)
        self.welcome()

    def create(self, name, description, start_date, periodicity):
        '''
        Create a new habit with the given name, description, start date, and periodicity.

        Args:
            name (str): The name of the habit.
            description (str): A brief description of the habit.
            start_date (str): The date when the habit started, in ISO format or 'now'.
            periodicity (str): The frequency of the habit, either 'daily' or 'weekly'.
        '''
        existing_habit = get_habit_by_name(self.habit_list, name) # Check if a habit with the same name already exists
        if existing_habit:
            print(f'{Fore.RED}A habit with the name {Fore.YELLOW}{name}{Fore.RED} already exists. Choose a different name.{Style.RESET_ALL}')
            return

        if periodicity not in ['daily', 'weekly']: # Check if the periodicity is valid
            print(f'{Fore.RED}Invalid periodicity. Supported values are: \'daily\' and \'weekly\'.{Style.RESET_ALL}')
            return

        try:
            if start_date.lower() == 'now': # If input is 'now', use the current date and time
                start_date = datetime.now()
            elif 'T' not in start_date: # If the input does not contain a time, use the current time
                start_date = datetime.fromisoformat(start_date)
                current_time = datetime.now().time()
                start_date = datetime.combine(start_date.date(), current_time)
            else:
                start_date = datetime.fromisoformat(start_date)
        except ValueError:
            print(f'{Fore.RED}Invalid start date. Valid date format: \'YYYY-MM-DD\' or \'YYYY-MM-DDTHH:MM:SS\'. Use \'now\' for current date and time.{Style.RESET_ALL}') # Check if the date is invalid
            return

        habit = create_habit(name, description, start_date, periodicity)
        self.habit_list.append(habit)
        save_info(self.habit_list, self.file_path)
        print(f'{Fore.GREEN}Habit {Fore.YELLOW}{name}{Fore.GREEN} created successfully{Style.RESET_ALL}')

    def edit(self, habit_name, name=None, description=None, start_date=None, periodicity=None):
        '''
        Edit an existing habit.

        Args:
            habit_name (str): The name of the habit to be edited.
            name (str, optional): The new name of the habit.
            description (str, optional): The new description of the habit.
            start_date (str, optional): The new start date of the habit in ISO format.
            periodicity (str, optional): The new frequency of the habit, either 'daily' or 'weekly'.
        '''
        habit = get_habit_by_name(self.habit_list, habit_name)
        if habit:
            if start_date:
                start_date = datetime.fromisoformat(start_date)
            edit_habit(habit, name=name, description=description, start_date=start_date, periodicity=periodicity)
            save_info(self.habit_list, self.file_path)
            print(f'{Fore.GREEN}Habit {Fore.YELLOW}{habit_name}{Fore.GREEN} edited successfully{Style.RESET_ALL}')
        else:
            raise Exception(f'{Fore.RED}Habit {Fore.YELLOW}{habit_name}{Fore.RED} not found{Style.RESET_ALL}')

    def delete(self, *habit_names): 
        '''
        Delete one or more habits.

        Args:
            *habit_names (str): The name(s) of the habit(s) to be deleted.
        '''
        if not habit_names:
            print(f'{Fore.RED}Provide at least one habit name to delete{Style.RESET_ALL}')
            return

        for habit_name in habit_names:
            habit = get_habit_by_name(self.habit_list, habit_name)
            if habit:
                delete_habit(self.habit_list, habit)
                save_info(self.habit_list, self.file_path)
                print(f'{Fore.GREEN}Habit {Fore.YELLOW}{habit_name}{Fore.GREEN} deleted successfully{Style.RESET_ALL}')
            else:
                raise ValueError(f'{Fore.RED}Habit {Fore.YELLOW}{habit_name}{Fore.RED} not found{Style.RESET_ALL}')

    def streak(self, habit_name):
        '''
        Calculate and return the current streak for a specific habit.
        
        Parameters:
        habit_name (str): The name of the habit to get the current streak for.
        
        Returns:
        str: A formatted string with the current streak for the specified habit.
        
        Raises:
        Exception: If the specified habit does not exist in the habit list.
        '''
        habit = get_habit_by_name(self.habit_list, habit_name)
        if habit:
            # Calculate current streak
            current_streak = streak_calc(habit)
            # Prepare the result string
            r_current_streak = f'{Fore.GREEN}Current streak for {Fore.YELLOW}{habit_name}{Fore.GREEN}: {Fore.WHITE}{current_streak}{Style.RESET_ALL}'
            return r_current_streak
        else:
            print(f'{Fore.RED}Habit {Fore.YELLOW}{habit_name}{Fore.RED} not found{Style.RESET_ALL}')
            # Raise an exception if the habit was not found
            raise Exception(f'{Fore.RED}Habit not found{Style.RESET_ALL}')

    def longest_streak(self, habit_name):
        '''
        Calculate and return the longest streak for a specific habit.
        
        Parameters:
        habit_name (str): The name of the habit to get the longest streak for.
        
        Returns:
        str: A formatted string with the longest streak for the specified habit.
        
        Raises:
        Exception: If the specified habit does not exist in the habit list.
        '''
        habit = get_habit_by_name(self.habit_list, habit_name)
        if habit:
            # Calculate the longest streak
            longest_streak = calculate_longest_streak(habit)
            # Prepare the result string depending on the habit's periodicity
            if habit.periodicity == 'daily':
                longest_streak_message = f'{Fore.GREEN}Longest streak for {Fore.YELLOW}{habit_name}{Fore.GREEN} is {Fore.WHITE}{longest_streak}{Fore.GREEN} days{Style.RESET_ALL}'
            elif habit.periodicity == 'weekly':
                longest_streak_message = f'{Fore.GREEN}Longest streak for {Fore.YELLOW}{habit_name}{Fore.GREEN} is {Fore.WHITE}{longest_streak}{Fore.GREEN} weeks{Style.RESET_ALL}'
            return longest_streak_message
        else:
            print(f'{Fore.RED}Habit {Fore.YELLOW}{habit_name}{Fore.RED} not found{Style.RESET_ALL}')
            # Raise an exception if the habit was not found
            raise Exception(f'{Fore.RED}Habit {Fore.YELLOW}{habit_name}{Fore.RED} not found{Style.RESET_ALL}')

    def longest_streak_all(self):
        '''Returns the longest streak for all habits.

        This method calculates the longest streak among all the habits and returns
        a formatted string message indicating the habit with the longest streak and
        the length of the streak.
        '''
        habit_with_max_streak, max_streak = longest_streak_all_habits(self.habit_list)
        longest_streak_message = f'{Fore.GREEN}{Style.BRIGHT}The habit with the longest streak is {Fore.YELLOW}{habit_with_max_streak}{Fore.GREEN} with a streak of {Fore.WHITE}{max_streak}{Fore.GREEN} days.{Style.RESET_ALL}'
        return longest_streak_message

    def all_habits(self):
        '''
        Retrieve and print all habits from the habit list.
        
        The method will output the total number of habits and the detailed information for each habit.
        '''
        all_habits = get_all_habits(self.habit_list)
        print(f'{Fore.YELLOW}Total habits: {Fore.WHITE}{len(all_habits)}{Style.RESET_ALL}')
        for habit in all_habits:
            print(f'{Fore.YELLOW}{habit.name}{Style.RESET_ALL} ({habit.description}, {Fore.CYAN}Periodicity: {habit.periodicity}{Style.RESET_ALL})')

    def filter(self, periodicity):
        '''
        Filter habits by periodicity and return a list of filtered habits.
        
        Parameters:
        periodicity (str): The periodicity filter ('daily' or 'weekly').

        Returns:
        list: A list of formatted strings for each habit that meets the filter condition.
        '''
        filtered_habits = habits_filter(self.habit_list, periodicity)
        print(f'{Fore.YELLOW}Total habits with {periodicity} periodicity: {Fore.WHITE}{len(filtered_habits)}{Style.RESET_ALL}')
        formatted_filters = []
        for habit in filtered_habits:
            formatted_filter = f'{Fore.YELLOW}{habit.name}{Style.RESET_ALL} ({habit.description}, {Fore.CYAN}Periodicity: {habit.periodicity}{Style.RESET_ALL})'
            formatted_filters.append(formatted_filter)
        return formatted_filters

    def completion_rates(self):
        '''
        Calculate and return the completion rates for all habits.
        
        Returns:
        list: A list of formatted strings for each habit's completion rate, or None if no habits are present.
        '''
        if not self.habit_list:
            print(Fore.RED + 'File not found or empty' + Style.RESET_ALL)
            return None
        else:
            rates = calculate_completion_rates(self.habit_list)
            formatted_rates = []
            for rate in rates:
                completion_rate = round(rate['completion_rate'], 2)
                rate['completion_rate'] = completion_rate
                formatted_rate = f"{Fore.YELLOW}{rate['habit_name']}{Fore.WHITE}: {Fore.WHITE}{completion_rate:.2f}%{Style.RESET_ALL}"
                formatted_rates.append(formatted_rate)
            return formatted_rates

    def complete(self, habit_name, completion_datetime=None):
        '''
        Mark a habit as complete at a specified datetime.
        
        Parameters:
        habit_name (str): The name of the habit to mark as complete.
        completion_datetime (str, optional): An ISO formatted datetime string. Defaults to the current datetime if not provided.
        
        Raises:
        Exception: If the specified habit does not exist in the habit list.
        '''
        habit = get_habit_by_name(self.habit_list, habit_name)
        if habit:
            if completion_datetime:
                completion_datetime = datetime.fromisoformat(completion_datetime) # If a completion datetime is provided, use it
            else:
                completion_datetime = datetime.now() # If no completion datetime is provided, use the current datetime
            habit.complete_habit(completion_datetime)
            save_info(self.habit_list, self.file_path)
            print(f'{Fore.GREEN}Habit {Fore.YELLOW}{habit_name}{Fore.GREEN} marked as complete{Style.RESET_ALL}')
        else:
            print(f'{Fore.RED}Habit {Fore.CYAN}{habit_name}{Fore.RED} not found{Style.RESET_ALL}')

    def welcome(self):
        '''
        Display a welcome message along with the basic commands for using the HabitBuddy application.
        '''
        print(f'{Fore.CYAN}\nWelcome to HabitBuddy!\n{Style.RESET_ALL}')


    def run(self):
        '''The main loop of the CLI application.
        This method runs the welcome message, then loops infinitely until the user
        inputs 'exit'. Within the loop, it reads command line input and invokes the
        corresponding class methods. If any exceptions are raised, they are caught
        and the error messages are printed out.
        '''
        self.welcome()
        fire.Fire(self)

if __name__ == "__main__":
    fire.Fire(HabitTrackerCLI)