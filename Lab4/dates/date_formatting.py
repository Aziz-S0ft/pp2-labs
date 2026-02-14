from datetime import datetime


def format_date(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def custom_format(dt: datetime) -> str:
    return dt.strftime("%d/%m/%Y")


def parse_date(date_string: str) -> datetime:
    return datetime.strptime(date_string, "%Y-%m-%d")


if __name__ == "__main__":
    now = datetime.now()

    print("Default format:", format_date(now))
    print("Custom format:", custom_format(now))

    parsed = parse_date("2026-02-14")
    print("Parsed date:", parsed)
