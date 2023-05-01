from datetime import datetime, timedelta

def streak_calc(habit):
    '''Calculate the current streak of a habit'''
    if not habit.completions:
        return 0

    def check_streak(current_date, completion_dates, delta_days):
        if current_date in completion_dates:
            return True, current_date - timedelta(days=delta_days)
        else:
            return False, current_date

    streak = 0
    today = datetime.now().date()
    current_date = today
    # Get a set of completion dates
    completion_dates = {completion.date() for completion in habit.completions}
    
    while current_date >= habit.start_date.date():
        if habit.periodicity == "daily":
            found, current_date = check_streak(current_date, completion_dates, 1)
        elif habit.periodicity == "weekly":
            week_start = current_date - timedelta(days=current_date.weekday())
            found = any(week_start <= date <= current_date for date in completion_dates)
            current_date = week_start - timedelta(days=1)
        else:
            raise ValueError("Invalid periodicity") # Raise an error if the periodicity is not supported
        if found:
            streak += 1
        else:
            break
    return streak

def habits_filter(habit_list, periodicity):
    '''Filter habits by periodicity'''
    return [habit for habit in habit_list if habit.periodicity == periodicity]

def generate_summary_report(habit_list):
    '''Generate a summary report of all habits'''
    return [{
        "habit_name": habit.name,
        "streak": streak_calc(habit),
        "total_completions": len(habit.completions)
    } for habit in habit_list]
