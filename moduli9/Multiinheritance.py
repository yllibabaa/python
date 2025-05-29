from email.utils import specialsre


class Vertebrate():
    def __init__(self,backtone=True):
        self.has_Backtone=backtone
    def vertebrate_info(self):
        print("vertebrates have a backtone")

class Aquatic:
    def __init__(self, habitat="water"):
        self.has_habitat = habitat
    def aquatic_info(self):
        print("aquatic animals live in water")

class Fish(Vertebrate,Aquatic):
    def __init__(self,species,backtone=True, habitat="water"):
        super().__init__(backtone=backtone)
        self.species=species
        self.habitat=habitat
    def fish_into(self):
        print(f"the {self.species} is a type of fish founf in {self.habitat}")
    def swim(self):
        print("the fish is swimming")

goldfish=Fish("goldfish")
print(goldfish.has_Backtone)
print(goldfish.habitat)
goldfish.vertebrate_info()