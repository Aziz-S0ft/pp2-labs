x = 300
def myfunc():
  print(x)
myfunc()
print(x)

x = 300
def myfunc():
  x = 200
  print(x)
myfunc()
print(x)


def myfunc():
  global x
  x = 300
myfunc()
print(x)

x = 300
def myfunc():
  global x
  x = 200
myfunc()
print(x)