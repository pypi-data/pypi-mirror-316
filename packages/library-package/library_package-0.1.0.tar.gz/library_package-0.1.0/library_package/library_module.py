

class Fruit:


    def __init__(self, fruit_name):   
        self.name = fruit_name

    def isInList(self):
        with open("library_package/resources/fruits.txt", "r") as file:
            fruits = " ".join(file.read().splitlines())  # separate lines with a single space

        return fruits.__contains__(self.name)

    


    

    

