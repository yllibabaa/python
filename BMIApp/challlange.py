from abc import ABC, abstractmethod

class Person(ABC):
    def __init__(self, name, age, weight, height):
        self.__name = name
        self.__age = age
        self.__weight = weight
        self.__height = height

    @property
    def name(self):
        return self.__name

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, age):
        self.__age = age

    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, weight):
        self.__weight = weight

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, height):
        self.__height = height

    @abstractmethod
    def calculate_bmi(self):
        pass

    @abstractmethod
    def get_bmi_category(self):
        pass

    @abstractmethod
    def print_info(self):
        pass


class Adult(Person):
    def __init__(self, name, age, height, weight):
        super().__init__(name, age, height, weight)
        self.__bmi = self.calculate_bmi()

    def calculate_bmi(self):
        # Using getter methods for weight and height
        weight = self.weight  # Get the weight using the getter
        height = self.height  # Get the height using the getter
        # BMI = weight (kg) / (height (m))^2
        return weight / (height / 100) ** 2  # Convert height to meters

    def get_bmi_category(self):
        bmi = self.__bmi
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 25:
            return "Normal weight"
        elif 25 <= bmi < 29.9:
            return "Overweight"
        else:
            return "Obese"

    def print_info(self):
        return {
            "name": self.name,
            "age": self.age,
            "weight": self.weight,
            "height": self.height,
            "bmi": self.__bmi,
            "category": self.get_bmi_category()
        }


class Child(Person):
    def __init__(self, name, age, height, weight):
        super().__init__(name, age, height, weight)
        self.__bmi = self.calculate_bmi()

    def calculate_bmi(self):
        weight = self.weight
        height = self.height
        return weight / (height / 100) ** 2

    def get_bmi_category(self):
        bmi = self.__bmi
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 25:
            return "Normal weight"
        elif 25 <= bmi < 29.9:
            return "Overweight"
        else:
            return "Obese"

    def print_info(self):
        return {
            "name": self.name,
            "age": self.age,
            "weight": self.weight,
            "height": self.height,
            "bmi": self.__bmi,
            "category": self.get_bmi_category()
        }



def get_user_input():
    name = input("Enter your name: ")
    age = int(input("Enter your age: "))
    height = float(input("Enter your height (in cm): "))
    weight = float(input("Enter your weight (in kg): "))
    return name, age, height, weight



def main():
    print("Please choose if you are an Adult or a Child:")
    person_type = input("Enter 'adult' or 'child': ").strip().lower()

    name, age, height, weight = get_user_input()

    if person_type == 'adult':
        adult = Adult(name, age, height, weight)
        info_adult = adult.print_info()
        print(f"Adult Info: {info_adult}")
    elif person_type == 'child':
        child = Child(name, age, height, weight)
        info_child = child.print_info()
        print(f"Child Info: {info_child}")
    else:
        print("Invalid input. Please enter 'adult' or 'child'.")


if __name__ == "__main__":
    main()
