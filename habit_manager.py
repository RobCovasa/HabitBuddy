from datetime import datetime, timedelta

class Habit:
    def __init__(self, name, description, start_date, periodicity):
        '''Constructor for the Habit class.'''
        self.name = name
        self.description = description
        self.start_date = start_date
        self.periodicity = periodicity
        self.completions = []

    def complete_habit(self, completion_datetime=None):
        '''Method to mark a habit as complete'''
        if completion_datetime is None:
            completion_datetime = datetime.now()
        self.completions.append(completion_datetime)

    def to_dictionary(self):
        '''Method to represent a habit as a dictionary.'''
        return {
            'name': self.name,
            'description': self.description,
            'start_date': self.start_date.isoformat(),
            'periodicity': self.periodicity,
            'completions': [completion.isoformat() for completion in self.completions], # Convert each completion datetime to a string
        }

    # Class method to create a Habit object from a dictionary
    @classmethod
    def from_dictionary(cls, habit_dict):
        '''Class method to create a Habit object from a dictionary.'''
        habit = cls(
            habit_dict['name'],
            habit_dict['description'],
            datetime.fromisoformat(habit_dict['start_date']),
            habit_dict['periodicity'],
        )
        habit.completions = [datetime.fromisoformat(completion) for completion in habit_dict['completions']] # Convert each completion string to a datetime
        return habit

    def get_past_completions(self, n): # n = number of days or weeks
        '''Method to get the past n days or weeks of completions.'''
        completions = []
        now = datetime.now()
        for i in range(n):
            if self.periodicity == "daily":
                target_date = now - timedelta(days=i)
            elif self.periodicity == "weekly":
                target_date = now - timedelta(weeks=i)

            # Check if the habit was completed on the target date
            completion = any([x.date() == target_date.date() for x in self.completions]) 
            completions.insert(0, completion)
        return completions

def create_habit(name, description, start_date, periodicity):
    '''Function to create a new habit.'''
    return Habit(name, description, start_date, periodicity)

def edit_habit(habit, name=None, description=None, start_date=None, periodicity=None): # if variable is None, it will not be changed
    '''Function to edit a habit.'''
    if name:
        habit.name = name
    if description:
        habit.description = description
    if start_date:
        habit.start_date = start_date
    if periodicity:
        habit.periodicity = periodicity

def delete_habit(habit_list, habit):
    '''Function to delete a habit.'''
    habit_list.remove(habit)

def get_habit_by_name(habit_list, name):
    '''Function to get a habit by its name.'''
    for habit in habit_list:
        if habit.name == name:
            return habit
    return None # None if the habit is not found