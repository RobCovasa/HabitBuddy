from datetime import datetime

def streak_calc(habit):
    '''Function to calculate the longest streak for a given habit.'''
    streak = 0
    max_streak = 0
    prev_completion = None

    for completion in sorted(habit.completions):
        if prev_completion:
            # habit == daily and the difference between the current and previous completion is 1 day, streak += 1
            if habit.periodicity == 'daily' and (completion - prev_completion).days == 1:
                streak += 1
            # habit == weekly and the difference between the current and previous completion is 7 days, streak += 1
            elif habit.periodicity == 'weekly' and (completion - prev_completion).days == 7:
                streak += 1
            else:
                # If the difference between the current and previous completion is not 1 day or 7 days, reset the streak
                streak = 1

            # Update the maximum streak
            if streak > max_streak:
                max_streak = streak

        prev_completion = completion

    return max_streak

def get_all_habits(habit_list):
    '''Function to return a list of all habits.'''
    return habit_list

def habits_filter(habit_list, periodicity):
    '''Function to return a list of habits filtered by periodicity.'''
    return list(filter(lambda habit: habit.periodicity == periodicity, habit_list))

def longest_streak_all_habits(habit_list):
    '''Function to return the habit with the longest streak.'''
    streaks = [(habit.name, streak_calc(habit)) for habit in habit_list]
    return max(streaks, key=lambda x: x[1])

def longest_streak_single_habit(habit):
    '''Function to return the longest streak for a given habit.'''
    return streak_calc(habit)

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