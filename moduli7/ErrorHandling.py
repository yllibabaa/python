from math import trunc
from traceback import print_tb

try:
    print("pjesto dy numra")
    nr1=int(input("shkruani nr1:"))
    nr2=int(input("shkruani nr2:"))
    resultati=nr1/nr2
    print("rezultati",resultati)
except ZeroDivisionError:
    print("ke gabu per shkak qe je duke pjestuar me 0")

    #second example.txt
    fruits={
        "apples":5,
        "banana":3,
        "orange":7
    }
    try:
        print(fruits["cherry"])
    except KeyError:
        print("the key dos not exist in dictionary")

        text="this is not the number"

        #third exeple
        try:
            text_to_int=int(text)
        except Exception as e:
            print("an error occorred while parsing the data:", e)


# fourtgh example.txt
try:
    resultati=10/2
except ZeroDivisionError:
    print("division by zero error occorred")
else:
    print("division successful,Result", resultati)

#fifth example.txt
try:
    resultati=10/0
except ZeroDivisionError:
    print("division zero occorred ")
finally:
    print("this part od code always runs")
    

