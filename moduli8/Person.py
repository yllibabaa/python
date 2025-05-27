class person:
    def __init__(self, name,age):
         self.name = name
         self.age = age

    def greet(self):
        print(f"hello i am {self.name},and i am {self.age}years old")

person1 = person("alice",15)
person2 = person("bob",15)

person1.greet()
person2.greet()