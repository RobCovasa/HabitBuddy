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

def calculate_completion_rates(habit_list):
    '''Calculate the completion rates of habits'''
    completion_rates = []
    
    for habit in habit_list:
        total_days = (datetime.now().date() - habit.start_date.date()).days
        if total_days <= 0:
            # Skip if the habit start date is in the future or today
            continue
        
        if habit.periodicity == "weekly":
            total_days = total_days // 7
        
        completion_rate = (len(habit.completions) / total_days) * 100
        completion_rates.append({
            "habit_name": habit.name,
            "completion_rate": completion_rate
        })
    
    return completion_rates