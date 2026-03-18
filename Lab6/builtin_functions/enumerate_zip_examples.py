# enumerate_zip_examples.py

names = ["Person1", "Person2", "Person3"]
scores = [95, 88, 76]

for index, name in enumerate(names, start=1):
    print(f"{index}. {name}")

for name, score in zip(names, scores):
    print(f"{name}: {score} points")

for i, (name, score) in enumerate(zip(names, scores), start=1):
    print(f"{i}. {name} scored {score}")
    
mixed = [1, "2", 3.0, True]
for item in mixed:
    print(f"{item} → type: {type(item)}")
    try:
        print("As float:", float(item))
    except ValueError:
        print("Cannot convert to float")