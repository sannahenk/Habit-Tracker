from datetime import datetime, timedelta
import json
from habit import Habit


def load_habits_from_json(file_path: str) -> list[Habit]:
    """loads habits from json, 
        arguments: file_path (str): path to json file with habit data
        returns list of habit instances loaded from json"""
    with open(file_path) as f:
        data = json.load(f)
        habits = []
        for item in data:
            habit = Habit(
                name=item["name"],
                periodicity=item["periodicity"],
                created_at=datetime.fromisoformat(item["created_at"]),
                completions=[datetime.fromisoformat(dt) for dt in item["completions"]]
            )
            habits.append(habit)
        return habits



class HabitTrackerService:
    """Service layer for managing habits.
    Responsibilities:
    - Load and save habits from/to JSON storage
    - Add new habits
    - List and retrieve habits
    - Complete habits
    - Perform analytics (streaks, periodicity filters)
    """

    def __init__(self):
        """initializes the habitracker service by loading habits from 'habits.json'."""
        self.habits = load_habits_from_json('habits.json')

    def save_habits_to_json(self):
        """saves habits to habits.json, each habit with name, periodicity, created at timestamp and completions timestamps"""
        with open('habits.json', 'w') as f:
            json.dump(
                [
                    {
                        "name": x.name,
                        "periodicity": x.periodicity,
                        "created_at": x.created_at.isoformat(),
                        "completions": [dt.isoformat() for dt in x.completions]
                    }
                    for x in self.habits
                ],
                f,
                indent=4
            )

    def add_habit(self, name: str, periodicity: str):
        """adds a habit
        arguments: name, periodicity
        ValueError if habit with same name already exists"""
        if self.get_habit_by_name(name) is not None:
            raise ValueError(f"Habit '{name}'already exists.")
        habit = Habit(name=name, periodicity=periodicity, created_at=datetime.now(), completions=[])
        self.habits.append(habit)

    def list_habits(self):
        """lists all habits
        returns: lsit of all habits"""
        return self.habits

    def get_habit_by_name(self, name: str):
        """retrieve habit by its name
        arguments: name
        returns: habit if found, otherwise none"""
        name = name.strip().lower()
        for habit in self.habits:
            if habit.name.strip().lower() == name:
                return habit
        return None

    def complete_habit(self, name: str):
        """completes a given habit
        arguments: name
        return: true = habit exists and marked complete, otherwise false"""
        name = name.strip().lower()
        for habit in self.habits:
            if habit.name.strip().lower() == name:
                habit.completions.append(datetime.now())
                return True
        return False
    
    def habits_by_periodicity(self, periodicity: str) -> list:
        """lists habits with given periodicity
        arguments: periodicity
        return: list of habits with desired periodicity"""
        periodicity = periodicity.strip().lower()
        return[habit for habit in self.habits if habit.periodicity.lower() == periodicity]
    
    def habit_with_longest_streak(self) -> tuple:
        """returns the habit with the longest streak + the streak length.
        return: tuple, habit with the longest streak + streak length, if no habit exists --> None, 0"""
        if not self.habits:
            return None, 0
        longest_habit = max(self.habits, key=lambda h: h.get_streak())
        return longest_habit, longest_habit.get_streak()

    