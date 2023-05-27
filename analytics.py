from datetime import datetime, timedelta

def streak_calc(habit):
    '''Function to calculate the current streak of a habit.'''
    
    if len(habit.completions) == 0:
        return 0

    current_date = datetime.now().date()
    current_streak = 0

    for completion_date in reversed(habit.completions):
        if isinstance(completion_date, str):
            completion_date = datetime.strptime(completion_date, "%Y-%m-%dT%H:%M:%S").date()
        else:
            completion_date = completion_date.date()
        if (current_date - completion_date).days > 1:
            break

        current_streak += 1
        current_date = completion_date

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

    if habit.periodicity == "daily":
        for i in range(1, len(completions)):
            if completions[i].date() - completions[i-1].date() == timedelta(days=1):
                current_streak += 1
            else:
                current_streak = 1
            
            if current_streak > longest_streak:
                longest_streak = current_streak
    elif habit.periodicity == "weekly":
        current_week_start = completions[0].date()
        for i in range(1, len(completions)):
            if completions[i].date() - completions[i-1].date() == timedelta(days=7):
                current_streak += 1
            else:
                current_streak = 1
                current_week_start = completions[i].date()
            
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
        if habit.periodicity == 'daily':
            completion_rate = (len(habit.completions) / total_days) * 100
        elif habit.periodicity == 'weekly':
            total_weeks = total_days // 7
            if total_days % 7 > 0:  # if the habit has started within the week
                total_weeks += 1
            completion_rate = (len(habit.completions) / total_weeks) * 100 if total_weeks > 0 else 0
        else:
            completion_rate = 0  # undefined periodicity

        rates.append({
            'habit_name': habit.name,
            'completion_rate': completion_rate
        })
    return rates