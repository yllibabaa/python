from ctypes import pythonapi


class Student:
    school_name = "digital school"
    #student_name ="Student"

    def __init__(self, name,age, course):
        self.name = name
        self.age = age
        self.course=course


student_1 = Student("alice",15,"python" )
print(student_1.course)

