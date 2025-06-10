from abs import Abc,abstractmethod

class Printable(abc)
    @abstractmethod
    def print_info(self):
        pass

class Book(Printable):
    def __init__(self,title,author):
        self.title=title
        self.author=author
    def print_info(self):
        print(f*f"book:{self.title} by {self.author}")
        libri=Book("hija e maleve","ismail kadare")
        libri.print.info()
