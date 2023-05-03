import fire
from colorama import Fore, Style
from datetime import datetime
from habit_manager import create_habit, edit_habit, delete_habit, get_habit_by_name
from analytics import streak_calc, habits_filter, generate_summary_report
from data_storage import load_info, save_info

class HabitTrackerCLI:
    def __init__(self, file_path="habits.json"):
        self.file_path = file_path
        self.habit_list = load_info(file_path)

    def create(self, name, description, start_date, periodicity):
        '''Create a new habit with the given name, description, start date, and periodicity.'''
        if periodicity not in ['daily', 'weekly']:
            print(f"{Fore.RED}Invalid periodicity. Supported values are: 'daily' and 'weekly'.{Style.RESET_ALL}")
        else:
            habit = create_habit(name, description, datetime.fromisoformat(start_date), periodicity)
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

    def delete(self, habit_name):
        '''Delete a habit with the given name.'''
        habit = get_habit_by_name(self.habit_list, habit_name)
        if habit:
            delete_habit(self.habit_list, habit)
            save_info(self.habit_list, self.file_path)
            print(f"{Fore.GREEN}Habit {Fore.CYAN}{habit_name}{Fore.GREEN} deleted successfully{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Habit {Fore.CYAN}{habit_name}{Fore.RED} not found{Style.RESET_ALL}")

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
            print(f"{habit.name} ({habit.description})")

    def report(self):
        '''Generate a summary report of all habits and print it.'''
        report = generate_summary_report(self.habit_list)
        for habit_report in report:
            print(Fore.YELLOW + f"{habit_report['habit_name']} - Streak: {habit_report['streak']} - Total Completions: {habit_report['total_completions']}")
            
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

if __name__ == "__main__":
    fire.Fire(HabitTrackerCLI)