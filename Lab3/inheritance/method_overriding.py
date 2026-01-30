
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name} say: ..."


class Dog(Animal):
    def speak(self):
        return f"{self.name} say: Гав-гав!"

class Cat(Animal):
    def speak(self):
        return f"{self.name} say: Мяу!"


dog = Dog("Ақтөс")
cat = Cat("Рыжик")

print(dog.speak()) 
print(cat.speak())  