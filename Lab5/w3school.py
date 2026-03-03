import re

txt = "The rain in Spain"
x = re.search("^The.*Spain$", txt)
print(x)
x = re.findall("ai", txt)
print(x)
x = re.search(r"\s", txt)
print("The first white-space character is located in position:", x.start())
x = re.split(r"\s", txt)
print(x)
x = re.sub(r"\s", "9", txt)
print(x)
x = re.search(r"\bS\w+", txt)
print(x.span())
x = re.search(r"\bS\w+", txt)
print(x.string)
x = re.search(r"\bS\w+", txt)
print(x.group())