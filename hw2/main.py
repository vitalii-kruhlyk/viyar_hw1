from datetime import timedelta
from datetime import date


def get_birthdays_per_week(users: list) -> dict[str, list[str]]:
    today = date.today()
    today_weekday = today.weekday()
    # if today is a weekend ignore saturday or/and sunday
    days_limit = 7 - (today_weekday - 4 if today_weekday > 4 else 0)

    result = {}
    for user_data in users:
        day_diff = (user_data["birthday"].replace(year=today.year) - today).days
        if 0 <= day_diff < days_limit:
            greet_day = today + timedelta(day_diff)
            # sun and sut -> monday
            if greet_day.weekday() > 4:
                greet_day += timedelta(days=(7 - greet_day.weekday()))

            result.setdefault(greet_day.strftime("%A"), []).append(user_data["name"])

    return result
