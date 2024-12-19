import os

class Fruit:


    def __init__(self, fruit_name):   
        self.name = fruit_name

    def isInList(self):
        current_dir = os.path.dirname(__file__)  # Geçerli dosyanın bulunduğu dizin
        file_path = os.path.join(current_dir, "resources\\fruits.txt")
        with open(file_path, "r") as file:
            fruits = " ".join(file.read().splitlines())  # separate lines with a single space

        return fruits.__contains__(self.name)

    

    

