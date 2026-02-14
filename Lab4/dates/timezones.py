from datetime import datetime
from zoneinfo import ZoneInfo


def get_time_in_timezone(timezone_name: str) -> datetime:
    return datetime.now(ZoneInfo(timezone_name))


if __name__ == "__main__":
    print("UTC:", get_time_in_timezone("UTC"))
    print("Almaty:", get_time_in_timezone("Asia/Almaty"))
    print("New York:", get_time_in_timezone("America/New_York"))
