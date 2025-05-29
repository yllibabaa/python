#class Superclass:

#class Subclass(Superclass): # Ketu subklasa trashegon prej superklases

class Animal: #this is a general
    def eat(self):
         print("This animal eats")
    def sleep(self):
         print("It sleeps")

class Bird(Animal):
    def fly(self):
        print("It flies in the sky")
    def sings(self):
        print("It sings")

bilbili=Bird()
bilbili.sings()
bilbili.fly()