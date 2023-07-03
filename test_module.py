import pytest
import shutil
from datetime import datetime
from unittest.mock import patch
from colorama import Fore, Style
from main import HabitTrackerCLI
from habit_manager import get_habit_by_name

# Constants
TEST_HABIT_NAME = "test habit"
TEST_DESCRIPTION = "testing"
TEST_START_DATE = "2022-01-01"
TEST_PERIODICITY_DAILY = "daily"
TEST_PERIODICITY_WEEKLY = "weekly"
INVALID_PERIODICITY = "invalid"
INVALID_DATE = "invalid date"
NEW_HABIT_NAME = "new name"
NEW_DESCRIPTION = "new description"
NEW_START_DATE = "2022-01-02"
EMPTY_STRING = ""
INVALID_PERIODICITY_FUTURE = "annually"

class TestHabitTracker:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        # Store a copy of the original habits.json file
        shutil.copyfile("habits.json", "habits_original.json")

        self.habit_tracker = HabitTrackerCLI()
        self.habit_tracker.habit_list.clear()  # Clear any habits loaded in the constructor
        yield
        self.habit_tracker.habit_list.clear()

        # Restore the original habits.json file
        shutil.move("habits_original.json", "habits.json")

    def test_create_habit(self):
        self.habit_tracker.create(TEST_HABIT_NAME, TEST_DESCRIPTION, TEST_START_DATE, TEST_PERIODICITY_DAILY)
        assert len(self.habit_tracker.habit_list) == 1, "Habit was not created."

    def test_create_habit_existing(self):
        self.habit_tracker.create(TEST_HABIT_NAME, TEST_DESCRIPTION, TEST_START_DATE, TEST_PERIODICITY_DAILY)
        self.habit_tracker.create(TEST_HABIT_NAME, TEST_DESCRIPTION, TEST_START_DATE, TEST_PERIODICITY_DAILY)
        assert len(self.habit_tracker.habit_list) == 1, "Existing habit was created."

    def test_create_habit_invalid_periodicity(self):
        self.habit_tracker.create(TEST_HABIT_NAME, TEST_DESCRIPTION, TEST_START_DATE, INVALID_PERIODICITY)
        assert len(self.habit_tracker.habit_list) == 0, "Habit with invalid periodicity was created."

    def test_create_habit_invalid_start_date(self, capsys):
        self.habit_tracker.create(TEST_HABIT_NAME, TEST_DESCRIPTION, INVALID_DATE, TEST_PERIODICITY_DAILY)
        captured = capsys.readouterr()
        assert "Invalid start date" in captured.out, "Habit with invalid start date was created."

    def test_edit_habit(self):
        self.habit_tracker.create(TEST_HABIT_NAME, TEST_DESCRIPTION, TEST_START_DATE, TEST_PERIODICITY_DAILY)
        self.habit_tracker.edit(
            TEST_HABIT_NAME,
            name=NEW_HABIT_NAME,
            description=NEW_DESCRIPTION,
            start_date=NEW_START_DATE,
            periodicity=TEST_PERIODICITY_WEEKLY
        )

        habit = get_habit_by_name(self.habit_tracker.habit_list, NEW_HABIT_NAME)
        
        assert habit.name == NEW_HABIT_NAME, "Habit name was not edited."
        assert habit.description == NEW_DESCRIPTION, "Habit description was not edited."
        assert habit.start_date == datetime.strptime(NEW_START_DATE, "%Y-%m-%d"), "Habit start date was not edited."
        assert habit.periodicity == TEST_PERIODICITY_WEEKLY, "Habit periodicity was not edited."

    def test_edit_habit_not_found(self):
        with pytest.raises(Exception): 
            self.habit_tracker.edit(
                TEST_HABIT_NAME,
                name=NEW_HABIT_NAME,
                description=NEW_DESCRIPTION,
                start_date=NEW_START_DATE,
                periodicity=TEST_PERIODICITY_WEEKLY
            )

    def test_delete_habit(self):
        self.habit_tracker.create(TEST_HABIT_NAME, TEST_DESCRIPTION, TEST_START_DATE, TEST_PERIODICITY_DAILY)
        self.habit_tracker.delete(TEST_HABIT_NAME)
        assert len(self.habit_tracker.habit_list) == 0, "Habit was not deleted."

    def test_delete_habit_not_found(self):
        with pytest.raises(Exception): 
            self.habit_tracker.delete(TEST_HABIT_NAME)

    def test_streak(self):
        self.habit_tracker.create(TEST_HABIT_NAME, TEST_DESCRIPTION, TEST_START_DATE, TEST_PERIODICITY_DAILY)
        self.habit_tracker.complete(TEST_HABIT_NAME)
        streak_message = self.habit_tracker.streak(TEST_HABIT_NAME)
        expected_message = f"{Fore.GREEN}Current streak for {Fore.YELLOW}{TEST_HABIT_NAME}{Fore.GREEN}: {Fore.WHITE}1{Style.RESET_ALL}"
        assert streak_message == expected_message, "Incorrect streak message."

    def test_streak_not_found(self):
        with pytest.raises(Exception): 
            self.habit_tracker.streak(TEST_HABIT_NAME)

    @patch('datetime.datetime')
    def test_calculate_completion_rates(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2023, 6, 1)
        mock_datetime.strptime.side_effect = lambda *args, **kw: datetime.strptime(*args, **kw)
        self.habit_tracker.create(TEST_HABIT_NAME, TEST_DESCRIPTION, TEST_START_DATE, TEST_PERIODICITY_DAILY)
        self.habit_tracker.complete(TEST_HABIT_NAME, "2023-05-01T10:00:00")
        completion_rates = self.habit_tracker.completion_rates()
        # Assuming completion rates are rounded to two decimal places
        expected_completion_rate = round(
            1 / ((datetime.now().date() - datetime.strptime(TEST_START_DATE, "%Y-%m-%d").date()).days + 1) * 100, 2
        )
        expected_formatted_string = (
            f"{Fore.YELLOW}{TEST_HABIT_NAME}{Fore.WHITE}: {Fore.WHITE}{expected_completion_rate:.2f}%{Style.RESET_ALL}"
        )
        assert completion_rates[0] == expected_formatted_string, "Incorrect completion rate calculated."
        
    def test_create_habit_empty_fields(self):
        self.habit_tracker.create(EMPTY_STRING, EMPTY_STRING, TEST_START_DATE, TEST_PERIODICITY_DAILY)
        assert len(self.habit_tracker.habit_list) == 0, "Habit with empty fields was created."

    def test_create_habit_invalid_periodicity_future(self):
        self.habit_tracker.create(TEST_HABIT_NAME, TEST_DESCRIPTION, TEST_START_DATE, INVALID_PERIODICITY_FUTURE)
        assert len(self.habit_tracker.habit_list) == 0, "Habit with future periodicity was created."

    def test_edit_habit_empty_fields(self):
        self.habit_tracker.create(TEST_HABIT_NAME, TEST_DESCRIPTION, TEST_START_DATE, TEST_PERIODICITY_DAILY)
        self.habit_tracker.edit(
            TEST_HABIT_NAME,
            name=EMPTY_STRING,
            description=EMPTY_STRING,
            start_date=TEST_START_DATE,
            periodicity=TEST_PERIODICITY_DAILY
        )
        habit = get_habit_by_name(self.habit_tracker.habit_list, TEST_HABIT_NAME)
        assert habit.name == TEST_HABIT_NAME, "Habit name was edited to an empty string."
        assert habit.description == TEST_DESCRIPTION, "Habit description was edited to an empty string."