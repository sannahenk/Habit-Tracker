# Habit Tracker

A simple Python-based habit tracker that allows you to manage habits with daily, weekly, or monthly periodicity. Track your progress, check streaks, and manage your habits easily.

## Features

- Add, complete, and view habits
- Track streaks for daily, weekly, and monthly habits
- List all habits or filter by periodicity
- Longest streak analysis for individual or all habits
- Load and select habits from a JSON file
- Predefined example habits with 4 weeks of data
- Unit tests for all core functionalities

## Requirements

- Python 3.10+
- See `requirements.txt` for dependencies

## Setup

1. Clone the repository.
2. \(Optional\) Create a virtual environment: `python3 -m venv .venv source .venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the application: `python main.py`

## Usage

- Habits are stored in `habits.json`.
- Use the CLI or provided functions to add, complete, and check streaks for habits.
- Example actions:
    1. Create a new habit
    2. List all habits
    3. Complete a habit
    4. Get streak of a habit
    5. Show habits by periodicity
    6. Show habit with the longest streak
- Run unit tests with: `python -m unittest discover tests`

## Project Structure

- `main.py` - CLI interface and main application logic
- `habit.py` – Habit data model and logic for individual habits
- `habittracker_service.py` – Business logic, JSON storage, and analytics functions
- `habits.json` - Habit data storage
- `test_habittracker.py` - Unit tests
