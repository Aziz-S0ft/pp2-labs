from functools import reduce

numbers = [1, 2, 3, 4, 5]

squared = list(map(lambda x: x**2, numbers))
print("Squared:", squared) 

even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print("Even numbers:", even_numbers)

sum_numbers = reduce(lambda x, y: x + y, numbers)
print("Sum of numbers:", sum_numbers) 

product_numbers = reduce(lambda x, y: x * y, numbers)
print("Product of numbers:", product_numbers)  

num_str = list(map(str, numbers))
print("Numbers as strings:", num_str) 

print("Type check:", type(numbers), type(num_str))