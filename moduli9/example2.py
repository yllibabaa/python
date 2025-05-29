class Animal:
    def sound(self):
        print("Generic animal sound")

class Dog(Animal):
    def sound(self):
        print("WOOF! WOOF!")

class Cat(Animal):
    def sound(self):
        print("Meow! Meow!")

kafshe=Animal()
kafshe.sound()

rex=Dog()
rex.sound()

tom=Cat()
tom.sound()