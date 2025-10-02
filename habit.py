from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class Habit:
    """= single habit with name, periodicity, creation date, and completion history
        attributes: name (habit name), periodicity (frequency), created_at (timestamp of creation) and completions (list of timestamps when completed)"""
    name: str
    periodicity: str
    created_at: datetime
    completions: list[datetime]

    def get_streak(self) -> int:
        """calculates current streak based on periodicity
            retunrs number of consecutive periods the habit has been completed (int)
            daily/weekly/monthly, if no completions --> 0"""
        if not self.completions:
            return 0
        completions = sorted(set(dt.date() for dt in self.completions), reverse=True)
        streak = 0
        today = datetime.now().date()

        if self.periodicity == "daily":
            for i, day in enumerate(completions):
                expected_day = today - timedelta(days=i)
                if day == expected_day:
                    streak += 1
                else:
                    break

        elif self.periodicity == "weekly":
            def week_key(d): return d.isocalendar()[0], d.isocalendar()[1]
            weeks = sorted(set(week_key(d) for d in completions), reverse=True)
            current_week = week_key(today)
            for i, week in enumerate(weeks):
                expected_week = (current_week[0], current_week[1] - i)
                # for the change in years 
                year, week_num = expected_week
                while week_num < 1:
                    year -= 1
                    week_num += datetime(year, 12, 28).isocalendar()[1]
                if week == (year, week_num):
                    streak += 1
                else:
                    break

        elif self.periodicity == "monthly":
            def month_key(d): return d.year, d.month
            months = sorted(set(month_key(d) for d in completions), reverse=True)
            current_month = (today.year, today.month)
            for i, month in enumerate(months):
                year, month_num = current_month
                month_num -= i
                while month_num < 1:
                    year -= 1
                    month_num += 12
                if month == (year, month_num):
                    streak += 1
                else:
                    break

        return streak
