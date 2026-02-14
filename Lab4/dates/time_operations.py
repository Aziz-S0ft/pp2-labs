from datetime import datetime, timedelta


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
