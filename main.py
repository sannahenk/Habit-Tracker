import questionary
from habittracker_service import HabitTrackerService

def main():
    """
    Main CLI loop for the Habit Tracker application.

    Provides a interface for users to:
    - Create new habits
    - List all habits
    - Complete habits
    - Check streaks
    - Filter habits by periodicity
    - Show habit with longest streak
    - Exit the application

    The function interacts with HabitTrackerService and handles user input/output.
    """
    service = HabitTrackerService()
    run = True

    while run:
        choice = questionary.select(
        "Choose an option:",
        choices=["Create Habit",
                 "List all Habits",
                 "Complete Habit",
                 "Get Streak of Habit",
                 "Show Habits by Periodicity", 
                 "Show Habit with longest Streak",
                 "Exit"]
        ).ask()

        if choice == "Exit":
            #save all habits befor exiting
            service.save_habits_to_json()
            run = False

        elif choice == "Create Habit":
            #creates new habit and stores it
            name = questionary.text("Enter habit name:").ask()
            periodicity = questionary.select(
                "Select periodicity:",
                choices=["daily", "weekly", "monthly"]
            ).ask()
            service.add_habit(name, periodicity)

        elif choice == "List all Habits":
            #lists all habits
            habits = service.list_habits()
            for habit in habits:
                print(f"Habit: {habit.name}, "
                      f"Periodicity: {habit.periodicity}, "
                      f"Created At: {habit.created_at}, "
                      f"Completions: {len(habit.completions)}")

        elif choice == "Complete Habit":
            #select a habit and mark it as complete
            habits = service.list_habits()
            if not habits:
                print("No habits found.")
            else:
                name = questionary.select(
                    "Select a habit to complete:",
                    choices=[habit.name for habit in habits]
                ).ask()
                if service.complete_habit(name):
                    print(f"Habit '{name}' marked as completed.")
                else:
                    print(f"Habit '{name}' not found.")

        elif choice == "Get Streak of Habit":
            #selects habit and shows current streak
            habits = service.list_habits()
            if not habits:
                print("No habits found.")
            else:
                name = questionary.select(
                    "Select a habit to get streak:",
                    choices=[habit.name for habit in habits]
                ).ask()
                habit = service.get_habit_by_name(name)
                if habit:
                    streak = habit.get_streak()
                    print(f"Habit '{name}' has a current streak of {streak}.")
                else:
                    print(f"Habit '{name}' not found.")
        
        elif choice == "Show Habits by Periodicity":
            #filter habits by their periodicity 
            periodicity = questionary.select(
                "Select Periodicity:", 
                choices=["daily", "weekly", "monthly"]
            ).ask()
            filtered = service.habits_by_periodicity(periodicity)
            if not filtered:
                print("No habits found.")
            else:
                for habit in filtered:
                    print(f"Habit: {habit.name}, Periodicity: {habit.periodicity}, Completions: {len(habit.completions)}")
        
        elif choice == "Show Habit with longest Streak":
            #show habit with longest streak and the streak length
            habit, streak = service.habit_with_longest_streak()
            if habit: 
                print(f"Habit '{habit.name}' has the longest  streak of {streak}.")
            else:
                print("No habits found")

if __name__ == "__main__":
    #runs CLI main loop when script is executed directly
    main()