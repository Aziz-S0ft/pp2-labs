def myfunc1():
  x = "Jane"
  def myfunc2():
    nonlocal x
    x = "hello"
    print(x)
  myfunc2()
  return x
print(myfunc1())