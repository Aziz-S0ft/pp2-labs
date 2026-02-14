from datetime import datetime, date, time


def create_date():
    return date(2026, 2, 14)


def create_time():
    return time(15, 30, 0)


def create_datetime():
    return datetime(2026, 2, 14, 15, 30)


def get_current_datetime():
    return datetime.now()


if __name__ == "__main__":
    print("Date:", create_date())
    print("Time:", create_time())
    print("Datetime:", create_datetime())
    print("Now:", get_current_datetime())