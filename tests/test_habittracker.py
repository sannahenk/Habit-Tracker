# test_habittracker.py
import pytest
from datetime import datetime, timedelta
from habittracker_service import HabitTrackerService
from habittracker_service import Habit
import json 

#resets JSON befor each test
@pytest.fixture(autouse=True)
def reset_json():
    #reset JSON befor test
    with open("habits.json", "w") as f:
        json.dump([], f)
    yield

@pytest.fixture
def service():
    #provides fresh instance of habitrackerservice for each test
    return HabitTrackerService()


def test_add_and_list_habits(service):
    #ensure habits can be added and listed 
    service.add_habit("Read", "daily")
    service.add_habit("Exercise", "weekly")
    habits = service.list_habits()
    assert len(habits) == 2
    assert habits[0].name == "Read"
    assert habits[1].periodicity == "weekly"


def test_add_duplicate_habit(service):
    #ensure addig a habit that is a duplicate will raise ValueError
    service.add_habit("Read", "daily")
    with pytest.raises(ValueError):
        service.add_habit("Read", "weekly")


def test_complete_habit(service):
    #verifies that completing habit updates 
    service.add_habit("Read", "daily")
    assert service.complete_habit("Read") is True
    habit = service.get_habit_by_name("Read")
    assert len(habit.completions) == 1


def test_complete_nonexistent_habit(service):
    #ensures completing non-existing habit returns false
    assert service.complete_habit("Nonexistent") is False


def test_get_streak_daily():
    #checks daily streak is calculated correctly
    habit = Habit("Read", "daily", created_at=datetime.now(), completions=[])
    today = datetime.now().date()
    habit.completions = [
        datetime.combine(today - timedelta(days=2), datetime.min.time()),
        datetime.combine(today - timedelta(days=1), datetime.min.time()),
        datetime.combine(today, datetime.min.time())
    ]
    assert habit.get_streak() == 3


def test_get_streak_daily_with_gap():
    #checks daily streak calc when a day is missing
    habit = Habit("Read", "daily", created_at=datetime.now(), completions=[])
    today = datetime.now().date()
    habit.completions = [
        datetime.combine(today - timedelta(days=3), datetime.min.time()),
        datetime.combine(today - timedelta(days=1), datetime.min.time()),
        datetime.combine(today, datetime.min.time())
    ]
    assert habit.get_streak() == 2


def test_get_streak_weekly():
    #verifies weekly streak calc
    habit = Habit("Exercise", "weekly", created_at=datetime.now(), completions=[])
    today = datetime.now().date()
    habit.completions = [
        datetime.combine(today - timedelta(weeks=2), datetime.min.time()),
        datetime.combine(today - timedelta(weeks=1), datetime.min.time()),
        datetime.combine(today, datetime.min.time())
    ]
    assert habit.get_streak() == 3


def test_get_streak_monthly():
    #verifies monthly streak calc
    habit = Habit("Pay Bills", "monthly", created_at=datetime.now(), completions=[])
    today = datetime.now().date()
    last_month = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
    two_months_ago = (last_month - timedelta(days=1)).replace(day=1)
    habit.completions = [
        datetime.combine(two_months_ago, datetime.min.time()),
        datetime.combine(last_month, datetime.min.time()),
        datetime.combine(today.replace(day=1), datetime.min.time())
    ]
    assert habit.get_streak() == 3


def test_get_streak_no_completions():
    #ensures that habits with no completions returns 0
    habit = Habit("Read", "daily", created_at=datetime.now(), completions=[])
    assert habit.get_streak() == 0


def test_get_habit_by_name(service):
    #verifies that habit can be retreived by name
    service.add_habit("Read", "daily")
    habit = service.get_habit_by_name("Read")
    assert habit is not None
    assert habit.name == "Read"


def test_get_habit_by_name_not_found(service):
    #ensures that querying non-existent habit returns none
    assert service.get_habit_by_name("Nonexistent") is None

def test_habits_by_periodicity(service):
    # test filtering by periodicity
    service.add_habit("Read", "daily")
    service.add_habit("Exercise", "weekly")
    service.add_habit("Pay Bills", "monthly")

    daily_habits = service.habits_by_periodicity("daily")
    weekly_habits = service.habits_by_periodicity("weekly")
    monthly_habits = service.habits_by_periodicity("monthly")

    assert len(daily_habits) == 1
    assert daily_habits[0].name == "Read"

    assert len(weekly_habits) == 1
    assert weekly_habits[0].name == "Exercise"

    assert len(monthly_habits) == 1
    assert monthly_habits[0].name == "Pay Bills"


def test_habit_with_longest_streak(service):
    # verifies that habit with longest streak is identiified correctly
    service.add_habit("Read", "daily")
    service.add_habit("Exercise", "weekly")

    # manually add completions to set streaks
    today = datetime.now().date()

    read = service.get_habit_by_name("Read")
    read.completions = [
        datetime.combine(today - timedelta(days=i), datetime.min.time())
        for i in range(4, -1, -1)  # last 5 days including today
    ]  # 5-day streak

    exercise = service.get_habit_by_name("Exercise")
    exercise.completions = [
        datetime.combine(today - timedelta(weeks=i), datetime.min.time())
        for i in range(2, -1, -1)  # last 3 weeks including this week
    ]  # 3-week streak

    habit, streak = service.habit_with_longest_streak()
    assert habit.name == "Read"
    assert streak == 5
