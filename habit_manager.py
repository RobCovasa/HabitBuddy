from datetime import datetime, timedelta

class Habit:
    def __init__(self, name, description, start_date, periodicity):
        '''
        Initialize a Habit object with name, description, start_date, and periodicity.

        Args:
            name (str): The name of the habit.
            description (str): A brief description of the habit.
            start_date (datetime): The date when the habit was started.
            periodicity (str): How often the habit occurs; 'daily' or 'weekly'.
        '''
        self.name = name
        self.description = description
        self.start_date = start_date
        self.periodicity = periodicity
        self.completions = []

    def __str__(self):
        '''Return a string representation of the Habit object, showing name and description.'''
        return f'{self.name} ({self.description})'

    def __repr__(self):
        '''Return a formal string representation of the Habit object, which can be used to reproduce the object.'''
        return self.__str__()

    def complete_habit(self, completion_datetime=None):
        '''
        Record a habit as completed by appending the completion datetime to the completions list.

        Args:
            completion_datetime (datetime, optional): The completion date and time. Defaults to the current datetime.
        '''
        if completion_datetime is None:
            completion_datetime = datetime.now()
        self.completions.append(completion_datetime)

    def to_dictionary(self):
        '''
        Convert the Habit object to a dictionary, useful for serialization.

        Returns:
            dict: A dictionary representation of the Habit object.
        '''
        return {
            'name': self.name,
            'description': self.description,
            'start_date': self.start_date.isoformat(),  # Convert datetime to string in ISO 8601 format
            'periodicity': self.periodicity,
            'completions': [completion.isoformat() for completion in self.completions],  # Convert datetime objects to strings
        }

    @classmethod
    def from_dictionary(cls, habit_dict):
        '''
        Create a Habit object from a dictionary, useful for deserialization.

        Args:
            habit_dict (dict): A dictionary representation of a Habit object.

        Returns:
            Habit: A new Habit object created from the dictionary.
        '''
        habit = cls(
            habit_dict['name'],
            habit_dict['description'],
            datetime.fromisoformat(habit_dict['start_date']),  # Convert string in ISO 8601 format to datetime
            habit_dict['periodicity'],
        )
        habit.completions = [datetime.fromisoformat(completion) for completion in habit_dict['completions']]  # Convert strings to datetime objects
        return habit

def create_habit(name, description, start_date, periodicity):
    '''
    Create a new Habit object and return it.

    Args:
        name (str): The name of the habit.
        description (str): A brief description of the habit.
        start_date (datetime): The date when the habit was started.
        periodicity (str): How often the habit occurs; 'daily' or 'weekly'.

    Returns:
        Habit: A new instance of the Habit class.
    '''
    return Habit(name, description, start_date, periodicity)

def edit_habit(habit, name=None, description=None, start_date=None, periodicity=None):
    '''
    Update the attributes of an existing Habit instance.

    Args:
        habit (Habit): The Habit instance to modify.
        name (str, optional): A new name for the habit. Defaults to None.
        description (str, optional): A new description for the habit. Defaults to None.
        start_date (datetime, optional): A new start date for the habit. Defaults to None.
        periodicity (str, optional): A new periodicity for the habit; either 'daily' or 'weekly'. Defaults to None.
    '''
    # Update the habit attributes only if a new value has been provided
    if name:
        habit.name = name
    if description:
        habit.description = description
    if start_date:
        habit.start_date = start_date
    if periodicity:
        habit.periodicity = periodicity

def delete_habit(habit_list, habit):
    '''
    Remove a Habit instance from the habit list.

    Args:
        habit_list (list): The list of habits.
        habit (Habit): The habit to delete.
    '''
    habit_list.remove(habit)

def get_habit_by_name(habit_list, name):
    '''
    Find and return a Habit instance from a list of habits, based on its name.

    Args:
        habit_list (list): A list of Habit instances.
        name (str): The name of the habit to retrieve.

    Returns:
        Habit or None: The Habit instance with the matching name, if it exists; None otherwise.
    '''
    # Loop through each habit in the list and return the one with the matching name
    for habit in habit_list:
        if habit.name == name:
            return habit
    return None