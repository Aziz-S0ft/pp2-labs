import json

# some JSON:
x =  '{ "name":"John", "age":30, "city":"New York"}'
# parse x:
y = json.loads(x)
# the result is a Python dictionary:
print(y["age"])


def parse_json_string(json_string: str):
    """
    Преобразует JSON-строку в Python объект (dict или list)
    """
    return json.loads(json_string)

if __name__ == "__main__":
    json_str = '{"name": "Aziz", "age": 17, "city": "Almaty"}'
    data = parse_json_string(json_str)
    print("Parsed JSON:", data)
    print("Name:", data["name"])
