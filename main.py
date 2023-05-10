import fire
from colorama import Fore, Style
from prettytable import PrettyTable
from datetime import datetime
from habit_manager import create_habit, edit_habit, delete_habit, get_habit_by_name
from analytics import streak_calc, habits_filter, calculate_completion_rates
from data_storage import load_info, save_info

class HabitTrackerCLI:
    def __init__(self, file_path="habits.json"):
        self.file_path = file_path
        self.habit_list = load_info(file_path)

    def create(self, name, description, start_date, periodicity):
        '''Create a new habit with the given name, description, start date, and periodicity.'''
        existing_habit = get_habit_by_name(self.habit_list, name)
        if existing_habit:
            print(f"{Fore.RED}A habit with the name {Fore.YELLOW}{name}{Fore.RED} already exists. Choose a different name.{Style.RESET_ALL}")
            return

        if periodicity not in ['daily', 'weekly']:
            print(f"{Fore.RED}Invalid periodicity. Supported values are: 'daily' and 'weekly'.{Style.RESET_ALL}")
            return

        try:
            start_date = datetime.fromisoformat(start_date) # Check if the date is valid
        except ValueError:
            print(f"{Fore.RED}Invalid start date. Valid date format: 'YYYY-MM-DD'.{Style.RESET_ALL}") # If not, print an error message
            return

        habit = create_habit(name, description, start_date, periodicity)
        self.habit_list.append(habit)
        save_info(self.habit_list, self.file_path)
        print(f"{Fore.GREEN}Habit {Fore.YELLOW}{name}{Fore.GREEN} created successfully{Style.RESET_ALL}")

    def edit(self, habit_name, name=None, description=None, start_date=None, periodicity=None):
        '''Edit a habit with the given name, description, start date, and periodicity.'''
        habit = get_habit_by_name(self.habit_list, habit_name)
        if habit:
            if start_date:
                start_date = datetime.fromisoformat(start_date)
            edit_habit(habit, name=name, description=description, start_date=start_date, periodicity=periodicity)
            save_info(self.habit_list, self.file_path)
            print(f"{Fore.GREEN}Habit {Fore.CYAN}'{habit_name}'{Fore.GREEN} edited successfully{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Habit {Fore.CYAN}{habit_name}{Fore.RED} not found{Style.RESET_ALL}")

    def delete(self, *habit_names):
        '''Delete habits with the given name or names.'''
        if not habit_names:
            print(f"{Fore.RED}Provide at least one habit name to delete{Style.RESET_ALL}")
            return

        for habit_name in habit_names:
            habit = get_habit_by_name(self.habit_list, habit_name)
            if habit:
                delete_habit(self.habit_list, habit)
                save_info(self.habit_list, self.file_path)
                print(f"{Fore.GREEN}Habit {Fore.YELLOW}{habit_name}{Fore.GREEN} deleted successfully{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Habit {Fore.YELLOWs}{habit_name}{Fore.RED} not found{Style.RESET_ALL}")

    def streak(self, habit_name):
        '''Get the current streak for a habit with the given name.'''
        habit = get_habit_by_name(self.habit_list, habit_name)
        if habit:
            print(f"{Fore.YELLOW}Current streak for habit '{habit_name}': {streak_calc(habit)}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Habit {Fore.CYAN}{habit_name}{Fore.RED} not found{Style.RESET_ALL}")

    def filter(self, periodicity):
        '''Filter habits by periodicity and print them.'''
        filtered_habits = habits_filter(self.habit_list, periodicity)
        for habit in filtered_habits:
            print(f"{Fore.YELLOW}{habit.name}{Style.RESET_ALL} ({habit.description})")

    def report(self):
        '''Generate a summary report of all habits and print it.'''
        # Check if habit list is empty
        if not self.habit_list:
            print(f"{Fore.RED}File not found or empty{Style.RESET_ALL}")
            return

        # Create a table with the habit data
        table_habits = PrettyTable()
        table_habits.field_names = ["Habit", "Description", "Periodicity", "Streak", "Completion (Last 7)"]

        for habit in self.habit_list:
            completions = habit.get_past_completions(7)
            circles = ""
            for completion in completions:
                if completion:
                    circles += f"{Fore.GREEN}●{Style.RESET_ALL} "
                else:
                    circles += f"{Fore.RED}●{Style.RESET_ALL} "
            
            # Add a row to the table for each habit
            table_habits.add_row([habit.name, habit.description, habit.periodicity, streak_calc(habit), circles])

        # Print the table
        print(table_habits)
                
    def completion_rates(self):
        '''Calculate and print the completion rates for all habits.'''
        if not self.habit_list:
            print(f"{Fore.RED}File not found or empty{Style.RESET_ALL}")
            return

        rates = calculate_completion_rates(self.habit_list)
        for rate in rates:
            print(f"{Fore.YELLOW}{rate['habit_name']}: {rate['completion_rate']:.2f}%{Style.RESET_ALL}")

            
    def complete(self, habit_name, completion_datetime=None):
        '''Mark a habit as complete.'''
        habit = get_habit_by_name(self.habit_list, habit_name)
        if habit:
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
        print("Welcome to HabitBuddy!")
        print(f"{Fore.WHITE}Here are the main commands:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  help{Fore.WHITE} - Show information about the available commands.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  exit{Fore.WHITE} - Quit the application.{Style.RESET_ALL}")

    def help(self):
        print(f"{Fore.WHITE}Available commands and their usage:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  create <name> <description> <start_date> <periodicity>{Fore.WHITE} - Create a new habit.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  edit <habit_name> [name] [description] [start_date] [periodicity]{Fore.WHITE} - Edit an existing habit.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  delete <habit_name>{Fore.WHITE} - Delete a habit.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  complete <habit_name> [completion_datetime]{Fore.WHITE} - Mark a habit as complete.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  streak <habit_name>{Fore.WHITE} - Get the current streak for a habit.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  filter <periodicity>{Fore.WHITE} - Filter habits by periodicity.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  report{Fore.WHITE} - Generate a summary report of all habits.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  completion_rates{Fore.WHITE} - Print the completion rates for all habits.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  help{Fore.WHITE} - Show this help message.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  exit{Fore.WHITE} - Quit the application.{Style.RESET_ALL}")

    def run(self):
        self.welcome()
        while True:
            command_line = input(f"{Fore.BLUE}> {Style.RESET_ALL}")
            if command_line.lower() == "exit":
                break
            try:
                fire.Fire({cmd: getattr(self, cmd) for cmd in dir(self) if not cmd.startswith('_')}, command_line)
            except Exception as e:
                print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")

if __name__ == "__main__":
    cli = HabitTrackerCLI()
    cli.run()