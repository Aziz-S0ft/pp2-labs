from datetime import datetime
from datetime import timedelta
from zoneinfo import ZoneInfo
now = datetime.now()
print(now)

print(now.strftime("%Y-%m-%d"))


def get_time_in_timezone(timezone_name: str) -> datetime:
    return datetime.now(ZoneInfo(timezone_name))


if __name__ == "__main__":
    print("UTC:", get_time_in_timezone("UTC"))
    print("Almaty:", get_time_in_timezone("Asia/Almaty"))
    print("New York:", get_time_in_timezone("America/New_York"))




def add_days(dt: datetime, days: int) -> datetime:
    return dt + timedelta(days=days)


def subtract_days(dt: datetime, days: int) -> datetime:
    return dt - timedelta(days=days)


def difference_in_days(dt1: datetime, dt2: datetime) -> int:
    return (dt1 - dt2).days


if __name__ == "__main__":
    now = datetime.now()
    future = add_days(now, 49)
    past = subtract_days(now, 5)

    print("Now:", now)
    print("Future:", future)
    print("Past:", past)
    print("Difference:", difference_in_days(future, now))
