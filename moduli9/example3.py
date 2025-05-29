class Animal:
    def __init__(self, name): # sshembulli per konstruktor dhe variabel e cila po inicializohet per kete klas
        self.name = name
    def sound(self):
        print("Generic animal sound")
    def desc(self):
        print(f"This animal name: {self.name}")

class Dog(Animal):
    def __init__(self, breed, name):#ketu eshte konstruktori i klases
        self.breed = breed#variabla qe vlen veq  per kit klas
        super().__init__()#ketu thirret konstruktori i superclass

    def sound(self):
        print("WOOF! WOOF!")

    def desc(self):
        super().desc()
        print(f"Breed: {self.breed}")

class Cat(Animal):
    def __init__(self, color, name):#ketu eshte konstruktori i klases
        self.color = color#variabla qe vlen veq  per kit klas
        super().__init__()#ketu thirret konstruktori i superclass

    def desc(self):
        super().desc()
        print(f"Color: {self.color}")

    def sound(self):
        print("Meow! Meow!")

rex=Dog("golden Retriver","rex")
rex.sound()
rex.desc()

cat=Cat("black","mia")
cat.sound()
cat.desc()


