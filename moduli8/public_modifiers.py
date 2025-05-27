class Myclass:

    def __init__(self):
        self.public_variable = "This is a public variable"

    def public_method(self):
        print("This is a puclic method")

my_class = Myclass()

print(my_class.public_variable)
my_class.public_method()