from email.policy import default

from lesson18 import next_shape
from pyexpat.errors import messages
total=0
for number in range(1,11):
    if number%2==0:
        total+number
        print("the sum of even numbers from 1 to 10 is",total)
        def greet():
            print("hello world")
            greet()
            def greet_person(name):
                print("hello ",name)
                greet_person("alma")
                def shuma(x,y):
                    z=x+y
                    return z
                resultati=shuma(3,4)
                print("3+4=",resultati)
def greet(name):
    message=f"hello,{name}!"
    print(message)
    greet("alma")

    def greet_person(name,greeting="hello"):
        message-f"{greeting},{name}"
        return message
    default_greeting=greet_person("alma")
    print(default_greeting)
    costum_greeting=greet_person()