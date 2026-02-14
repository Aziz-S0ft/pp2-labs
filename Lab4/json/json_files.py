import json

def read_json_file(filename: str):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json_file(filename: str, data: dict):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    # читаем файл
    data = read_json_file("/Users/aziz/Python/pp2-labs/Lab4/json/sample-data.json")

    print("Data from file:", data)

    # изменяем и сохраняем
    data["new_field"] = "Hello"
    data['cars']=['None','Lexus 570 lx','Mersedes CLS 6.3 AMG']
    write_json_file("/Users/aziz/Python/pp2-labs/Lab4/json/sample-data.json", data)
    print("File updated!")
