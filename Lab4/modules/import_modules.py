import create_module
import my_module
create_module.greeting('Aziz')
print(create_module.person1)
a = create_module.person1["age"]
print(a)

my_car=my_module.car('Mersedes','CLS')
my_car.info()

import platform

x = dir(platform)
print(x)