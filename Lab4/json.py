import json

data = '{"name": "Aziz", "age": 18}'
parsed = json.loads(data)

json_string = json.dumps(parsed)

with open("sample-data.json") as f:
    data = json.load(f)
with open("output.json", "w") as f:
    json.dump(data, f)