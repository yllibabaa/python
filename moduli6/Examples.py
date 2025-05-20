from moduli6.my_math import katrori
import math as m
y=katrori(5)
print(f"Katrori i numrit 5 eshte {y}")

resultati=m.sqrt(5)
print(f"Katrori i numrit 5 ehste  {resultati}")


from my_package import modul1 as m1
from my_package import modul2 as m2
from my_package import modul3 as m3

m1.hello()
m2.greet()
m3.welcome()

import emoji
print(emoji.emojize("Python is fun :snake:"))