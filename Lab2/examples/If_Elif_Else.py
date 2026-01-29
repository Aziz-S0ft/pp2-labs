a = 33
b = 200
if b > a:
  print("b is greater than a")
elif a == b:
  print("a and b are equal")
else:
  print("a is greater than b")

is_logged_in = True
if is_logged_in:
  print("Welcome back!")



score = 75

if score >= 90:
  print("Grade: A")
elif score >= 80:
  print("Grade: B")
elif score >= 70:
  print("Grade: C")
elif score >= 60:
  print("Grade: D")

if a > b: print("a is greater than b")
bigger = a if a > b else b
print("Bigger is", bigger)
print("A") if a > b else print("=") if a == b else print("B")
c = 500
if a > b and c > a:
  print("Both conditions are True")
x = 41

if x > 10:
  print("Above ten,")
  if x > 20:
    print("and also above 20!")
  else:
    print("but not above 20.")
if b > a:
  pass