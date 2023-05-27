import fire
from colorama import Fore, Style
from datetime import datetime
from habit_manager import create_habit, edit_habit, delete_habit, get_habit_by_name
from analytics import streak_calc, habits_filter, calculate_completion_rates, get_all_habits, calculate_longest_streak, longest_streak_all_habits
from data_storage import load_info, save_info

# Main Class for Habit Tracker Command Line Interface
class HabitTrackerCLI:
    def __init__(self, file_path="habits.json"):
        self.file_path = file_path
        self.habit_list = load_info(file_path)
        
    def __str__(self):
        return f"{self.name} ({self.description})"

    def __repr__(self):
        return self.__str__()

    def create(self, name, description, start_date, periodicity):
        '''Method to create a new habit with the given name, description, start date, and periodicity.'''
        
        # Check if a habit with the same name already exists
        existing_habit = get_habit_by_name(self.habit_list, name)
        
        if existing_habit:
            print(f"{Fore.RED}A habit with the name {Fore.YELLOW}{name}{Fore.RED} already exists. Choose a different name.{Style.RESET_ALL}")
            return

        # Check if the periodicity is valid
        if periodicity not in ['daily', 'weekly']:
            print(f"{Fore.RED}Invalid periodicity. Supported values are: 'daily' and 'weekly'.{Style.RESET_ALL}")
            return

        try:
            # If start_date == 'now', use the current datetime
            if start_date.lower() == 'now':
                start_date = datetime.now()
            # If there is no time component, add the current time
            elif 'T' not in start_date:
                start_date = datetime.fromisoformat(start_date)
                current_time = datetime.now().time()
                start_date = datetime.combine(start_date.date(), current_time)
            else:
                # If a time component is present, parse it as is
                start_date = datetime.fromisoformat(start_date)
        except ValueError:
            # If the start_date is not valid, print an error message
            print(f"{Fore.RED}Invalid start date. Valid date format: 'YYYY-MM-DD' or 'YYYY-MM-DDTHH:MM:SS'. Use 'now' for current date and time.{Style.RESET_ALL}")
            return

        habit = create_habit(name, description, start_date, periodicity)
        self.habit_list.append(habit)
        save_info(self.habit_list, self.file_path)
        print(f"{Fore.GREEN}Habit {Fore.YELLOW}{name}{Fore.GREEN} created successfully{Style.RESET_ALL}")

    def edit(self, habit_name, name=None, description=None, start_date=None, periodicity=None):
        '''Method to edit a habit.'''
        habit = get_habit_by_name(self.habit_list, habit_name)
        if habit:
            if start_date:
                start_date = datetime.fromisoformat(start_date)
            edit_habit(habit, name=name, description=description, start_date=start_date, periodicity=periodicity)
            save_info(self.habit_list, self.file_path)
            print(f"{Fore.CYAN}Habit {Fore.YELLOW}'{habit_name}'{Fore.CYAN} edited successfully{Style.RESET_ALL}")
        else:
            raise Exception(f"{Fore.RED}Habit {Fore.YELLOW}{habit_name}{Fore.RED} not found{Style.RESET_ALL}")

    def delete(self, *habit_names): # Delete one or more habits at once
        '''Method to delete a habit.'''
        if not habit_names:
            print(f"{Fore.RED}Provide at least one habit name to delete{Style.RESET_ALL}")
            return

        for habit_name in habit_names:
            habit = get_habit_by_name(self.habit_list, habit_name)
            if habit:
                delete_habit(self.habit_list, habit)
                save_info(self.habit_list, self.file_path)
                print(f"{Fore.MAGENTA}Habit {Fore.YELLOW}{habit_name}{Fore.MAGENTA} deleted successfully{Style.RESET_ALL}")
            else:
                raise ValueError(f"{Fore.RED}Habit {Fore.YELLOW}{habit_name}{Fore.RED} not found{Style.RESET_ALL}")

    def streak(self, habit_name):
        '''Method to get the current streak for a given habit.'''
        habit = get_habit_by_name(self.habit_list, habit_name)
        if habit:
            current_streak = streak_calc(habit)
            r_current_streak = f"{Fore.CYAN}Current streak for {Fore.WHITE}'{habit_name}': {Fore.CYAN}{current_streak}{Style.RESET_ALL}"
            return r_current_streak  # Return the formatted string
        else:
            print(f"{Fore.RED}Habit {Fore.YELLOW}{habit_name}{Fore.RED} not found{Style.RESET_ALL}")
            raise Exception(f"{Fore.RED}Habit not found{Style.RESET_ALL}")

    def longest_streak(self, habit_name):
        '''Method to get the longest streak for a given habit.'''
        habit = get_habit_by_name(self.habit_list, habit_name)
        if habit:
            longest_streak = calculate_longest_streak(habit)
            if habit.periodicity == "daily":
                longest_streak_message = f"{Fore.GREEN}Longest streak for {Fore.YELLOW}{habit_name}{Fore.GREEN} is {longest_streak} days{Style.RESET_ALL}"
            elif habit.periodicity == "weekly":
                longest_streak_message = f"{Fore.GREEN}Longest streak for {Fore.YELLOW}{habit_name}{Fore.GREEN} is {longest_streak} weeks{Style.RESET_ALL}"
            return longest_streak_message  # Return the formatted message
        else:
            print(f"{Fore.RED}Habit {Fore.YELLOW}{habit_name}{Fore.RED} not found{Style.RESET_ALL}")
            raise Exception(f"{Fore.RED}Habit {Fore.YELLOW}{habit_name}{Fore.RED} not found{Style.RESET_ALL}")

    def longest_streak_all(self):
        '''Method to get the longest streak for all habits.'''
        habit_with_max_streak, max_streak = longest_streak_all_habits(self.habit_list)
        longest_streak_message = f"{Fore.GREEN}{Style.BRIGHT}The habit with the longest streak is {Fore.YELLOW}'{habit_with_max_streak}'{Fore.GREEN} with a streak of {Fore.YELLOW}{max_streak}{Fore.GREEN} days.{Style.RESET_ALL}"
        return longest_streak_message

    def all_habits(self):
        '''Method to print all habits.'''
        all_habits = get_all_habits(self.habit_list)
        print(f"{Fore.CYAN}Total habits: {len(all_habits)}{Style.RESET_ALL}")
        for habit in all_habits:
            print(f"{Fore.YELLOW}{habit.name}{Style.RESET_ALL} ({habit.description}, {Fore.CYAN}Periodicity: {habit.periodicity}{Style.RESET_ALL})")

    def filter(self, periodicity):
        '''Method to filter habits by periodicity.'''
        filtered_habits = habits_filter(self.habit_list, periodicity)
        print(f"{Fore.CYAN}Total habits with {periodicity} periodicity: {len(filtered_habits)}{Style.RESET_ALL}")
        formatted_filters = []
        for habit in filtered_habits:
            formatted_filter = f"{Fore.YELLOW}{habit.name}{Style.RESET_ALL} ({habit.description}, {Fore.CYAN}Periodicity: {habit.periodicity}{Style.RESET_ALL})"
            formatted_filters.append(formatted_filter)
        return formatted_filters

    def completion_rates(self):
        '''Method to calculate and return the completion rates for all habits.'''
        if not self.habit_list:
            print(Fore.RED + "File not found or empty" + Style.RESET_ALL)
            return None
        else:
            rates = calculate_completion_rates(self.habit_list)
            formatted_rates = []
            for rate in rates:
                completion_rate = round(rate['completion_rate'], 2)
                rate['completion_rate'] = completion_rate
                formatted_rate = f"{Fore.YELLOW}{rate['habit_name']}{Fore.WHITE}: {Fore.GREEN}{completion_rate:.2f}%{Style.RESET_ALL}"
                formatted_rates.append(formatted_rate)  # Append the formatted string
            return formatted_rates  # return formatted data

    def complete(self, habit_name, completion_datetime=None):
        '''Method to mark a habit as complete.'''
        habit = get_habit_by_name(self.habit_list, habit_name)
        if habit:
            # If a completion datetime is provided, parse it
            if completion_datetime:
                completion_datetime = datetime.fromisoformat(completion_datetime)
            else:
                # Default to system datetime
                completion_datetime = datetime.now()
            habit.complete_habit(completion_datetime)
            save_info(self.habit_list, self.file_path)
            print(f"{Fore.GREEN}Habit {Fore.CYAN}{habit_name}{Fore.GREEN} marked as complete{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Habit {Fore.CYAN}{habit_name}{Fore.RED} not found{Style.RESET_ALL}")

    def welcome(self):
        '''Method to print the welcome message'''
        print("Welcome to HabitBuddy!")
        print(f"{Fore.WHITE}Here are the main commands:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  help{Fore.WHITE} - Show information about the available commands.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  exit{Fore.WHITE} - Quit the application.{Style.RESET_ALL}")

    def help(self):
        '''Method to print the help message.'''
        print(f"{Fore.WHITE}Available commands and their usage:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  create <name> <description> <start_date> <periodicity>{Fore.WHITE} - Create a new habit.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  edit <habit_name> [name] [description] [start_date] [periodicity]{Fore.WHITE} - Edit an existing habit.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  delete <habit_name>{Fore.WHITE} - Delete a habit.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  complete <habit_name> [completion_datetime]{Fore.WHITE} - Mark a habit as complete.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  streak <habit_name>{Fore.WHITE} - Get the current streak for a habit.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  longest_streak_all{Fore.WHITE} - Get the habit with the longest streak.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  longest_streak <habit_name>{Fore.WHITE} - Get the longest streak for a given habit.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  all_habits{Fore.WHITE} - Get all habits.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  filter <periodicity>{Fore.WHITE} - Filter habits by periodicity.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  completion_rates{Fore.WHITE} - Print the completion rates for all habits.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  welcome{Fore.WHITE} - Print the welcome message.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  help{Fore.WHITE} - Show this help message.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  exit{Fore.WHITE} - Quit the application.{Style.RESET_ALL}")

    def run(self):
        '''Method to loop the CLI.'''
        self.welcome()
        while True:
            command_line = input(f"{Fore.BLUE}> {Style.RESET_ALL}")
            if command_line.lower() == "exit":
                break
            try:
                fire.Fire({cmd: getattr(self, cmd) for cmd in dir(self) if not cmd.startswith('_')}, command_line)
            # Catch ValueError if the command is invalid or the parameters are invalid
            except ValueError as e:
                print(f"{Fore.RED}Invalid command or parameters: {str(e)}{Style.RESET_ALL}")
            # Catch AttributeError if the command is not found
            except AttributeError as e:
                print(f"{Fore.RED}Command not found: {str(e)}{Style.RESET_ALL}")
            # Catch Exception for any other errors
            except Exception as e:
                print(f"{Fore.RED}An unexpected error occurred: {str(e)}{Style.RESET_ALL}")

if __name__ == "__main__":
    cli = HabitTrackerCLI()
    cli.run()