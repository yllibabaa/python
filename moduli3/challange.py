
gpa=3.5
score=65

if gpa>=3.5 and score == 65:
    print("You have a full scholarship")
elif gpa>=3.5 and 50<=score<=65:
    print("You have a partial scholarship")
elif gpa>=3.5 and score<=50:
    print("You are not eligable for a scholarship")
elif gpa<=3.5:
    print("You are not eligable for a scholarship")
else:
    print("Error")

