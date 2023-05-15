from datetime import datetime, timedelta

def streak_calc(habit):
    """Function to calculate the current streak of a habit."""
    
    if len(habit.completions) == 0:
        return 0
    
    current_streak = 0
    today = datetime.now()
    for i in range(len(habit.completions)-1, -1, -1):
        completion_date = habit.completions[i]
        if today.date() - completion_date.date() > timedelta(days=1):
            break
        current_streak += 1
        today = completion_date

    return current_streak

def get_all_habits(habit_list):
    '''Function to return a list of all habits.'''
    return habit_list

def habits_filter(habit_list, periodicity):
    '''Function to return a list of habits filtered by periodicity.'''
    return list(filter(lambda habit: habit.periodicity == periodicity, habit_list))

def calculate_longest_streak(habit):
    '''Function to calculate the longest streak of a habit.'''
    longest_streak = 1
    current_streak = 1
    completions = sorted([datetime.fromisoformat(completion) if isinstance(completion, str) else completion for completion in habit.completions])
    for i in range(1, len(completions)):
        if completions[i].date() - completions[i-1].date() == timedelta(days=1):
            current_streak += 1
        else:
            current_streak = 1
        
        if current_streak > longest_streak:
            longest_streak = current_streak

    return longest_streak

def longest_streak_all_habits(habit_list):
    '''Function to return the habit with the longest streak.'''
    streaks = [(habit.name, calculate_longest_streak(habit)) for habit in habit_list]
    return max(streaks, key=lambda x: x[1])

def calculate_completion_rates(habit_list):
    '''Function to calculate the completion rates for all habits.'''
    rates = []
    for habit in habit_list:
        total_days = (datetime.now().date() - habit.start_date.date()).days + 1
        completion_rate = (len(habit.completions) / total_days) * 100
        rates.append({
            'habit_name': habit.name,
            'completion_rate': completion_rate
        })
    return rates