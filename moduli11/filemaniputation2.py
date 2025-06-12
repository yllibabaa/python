import os
if os.path.exists("example.txt"):
    print("file exists")

name="alma"
age=50

with open("uotput.txt","w")as file:
    file.write("name:"+name+"\n")
    file.write("name:"+name+"\n")