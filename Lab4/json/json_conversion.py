import json

def convert_to_json(obj: dict) -> str:
    """
    Преобразует Python объект (dict, list) в JSON-строку
    """
    return json.dumps(obj, indent=4)  # красивое форматирование


if __name__ == "__main__":
    person = {"name": "Aziz", "age": 17, "city": "Almaty"}
    json_str = convert_to_json(person)
    print("JSON String:\n", json_str)