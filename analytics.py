from datetime import datetime, timedelta

def streak_calc(habit):
    '''
    Calculate the current streak of a habit.

    Args:
        habit (object): Habit object containing habit information and completions.

    Returns:
        int: Current streak of the habit.
    '''
    # If habit has no completions, return streak as 0
    if len(habit.completions) == 0:
        return 0

    current_date = datetime.now().date()
    current_streak = 0

    for completion_date in reversed(habit.completions): # Iterate through completions in reverse order
        if isinstance(completion_date, str):
            completion_date = datetime.strptime(completion_date, '%Y-%m-%dT%H:%M:%S').date()
        else:
            completion_date = completion_date.date()

        if (current_date - completion_date).days > 1: # If the habit was not completed the previous day, break
            break

        current_streak += 1 # Increment streak if habit was completed the previous day
        current_date = completion_date

    return current_streak


def get_all_habits(habit_list):
    '''
    A function that returns the inputted habit list.

    Args:
        habit_list (list): List of all habits.

    Returns:
        list: Inputted list of all habits.
    '''
    return habit_list


def habits_filter(habit_list, periodicity):
    '''
    Filter habits by their periodicity.

    Args:
        habit_list (list): List of all habits.
        periodicity (str): The periodicity to filter habits by.

    Returns:
        list: Habits with the given periodicity.
    '''
    return list(filter(lambda habit: habit.periodicity == periodicity, habit_list))


def calculate_longest_streak(habit):
    '''
    Calculate the longest streak of a habit.

    Args:
        habit (object): Habit object containing habit information and completions.

    Returns:
        int: Longest streak of the habit.
    '''
    longest_streak = current_streak = 1

    completions = sorted([datetime.fromisoformat(completion) if isinstance(completion, str) else completion for completion in habit.completions])

    if habit.periodicity == 'daily': # If the habit is to be completed daily, increment current_streak if the habit was completed on consecutive days
        for i in range(1, len(completions)):
            if completions[i].date() - completions[i-1].date() == timedelta(days=1):
                current_streak += 1
            else:
                current_streak = 1

            longest_streak = max(longest_streak, current_streak)

    elif habit.periodicity == 'weekly': # If the habit is to be completed weekly, increment current_streak if the habit was completed on consecutive weeks
        for i in range(1, len(completions)):
            if completions[i].date() - completions[i-1].date() == timedelta(days=7):
                current_streak += 1
            else:
                current_streak = 1

            longest_streak = max(longest_streak, current_streak)

    return longest_streak

def longest_streak_all_habits(habit_list):
    '''
    Determine the habit with the longest streak.

    Args:
        habit_list (list): List of all habits.

    Returns:
        tuple: Habit with the longest streak and the streak length.
    '''
    streaks = [(habit.name, calculate_longest_streak(habit)) for habit in habit_list]
    return max(streaks, key=lambda x: x[1])


def calculate_completion_rates(habit_list):
    '''
    Calculate the completion rates for all habits.

    Args:
        habit_list (list): List of Habit objects, each representing a habit.

    Returns:
        list: A list of dictionaries, each containing a habit's name and its corresponding completion rate.
    '''
    rates = []

    for habit in habit_list:
        total_days = (datetime.now().date() - habit.start_date.date()).days + 1

        if habit.periodicity == 'daily':
            completion_rate = (len(habit.completions) / total_days) * 100 

        elif habit.periodicity == 'weekly':
            total_weeks = total_days // 7
            if total_days % 7 > 0:
                total_weeks += 1

            completion_rate = (len(habit.completions) / total_weeks) * 100 if total_weeks > 0 else 0

        else:
            completion_rate = 0 # If the habit is not daily or weekly, set the completion rate to 0

        rates.append({
            'habit_name': habit.name,
            'completion_rate': completion_rate
        })

    return rates