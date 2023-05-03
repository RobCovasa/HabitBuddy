from datetime import datetime # Used to store completion dates

class Habit:
    def __init__(self, name, description, start_date, periodicity):
        '''Create a new habit.'''
        self.name = name
        self.description = description
        self.start_date = start_date
        self.periodicity = periodicity
        self.completions = [] # Creates an empty list of completions for the habit
        
    def complete_habit(self, completion_datetime=None):
        '''Add a completion to the habit.'''
        if completion_datetime is None:
            completion_datetime = datetime.now()
        self.completions.append(completion_datetime)

    def to_dictionary(self):
        '''Return a dictionary representation of the habit.'''
        return {
            'name': self.name,
            'description': self.description,
            'start_date': self.start_date.isoformat(),
            'periodicity': self.periodicity,
            'completions': [completion.isoformat() for completion in self.completions], # Convert datetimes to strings (format ISO 8601)
        }

    @classmethod
    def from_dictionary(cls, habit_dict):
        '''Create a habit from a dictionary representation.'''
        habit = cls(
            habit_dict['name'],
            habit_dict['description'],
            datetime.fromisoformat(habit_dict['start_date']),
            habit_dict['periodicity'],
        )
        habit.completions = [datetime.fromisoformat(completion) for completion in habit_dict['completions']]
        return habit

def create_habit(name, description, start_date, periodicity):
    '''Creates a new habit.'''
    return Habit(name, description, start_date, periodicity)

def edit_habit(habit, name=None, description=None, start_date=None, periodicity=None):
    '''Edit a habit.'''
    if name:
        habit.name = name
    if description:
        habit.description = description
    if start_date:
        habit.start_date = start_date
    if periodicity:
        habit.periodicity = periodicity

def delete_habit(habit_list, habit):
    '''Delete a habit.'''
    habit_list.remove(habit)

def get_habit_by_name(habit_list, name):
    '''Return a habit with the given name.'''
    for habit in habit_list:
        if habit.name == name:
            return habit
    return None # No habit with the given name was found