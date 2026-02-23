numbers = [1, 2, 3]
it = iter(numbers)

print(next(it))
print(next(it))
print(next(it))

def my_generator():
    for i in range(5):
        yield i

gen = (x * 2 for x in range(5))



class MyNumbers:
  def __iter__(self):
    self.a = 1
    return self

  def __next__(self):
    x = self.a
    self.a += 5
    return x

myclass = MyNumbers()
myiter = iter(myclass)

print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))

mytuple = ("apple", "banana", "cherry")

for x in mytuple:
  print(x)

mystr = "banana"

for x in mystr:
  print(x)