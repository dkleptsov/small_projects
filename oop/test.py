def main():
    class Habbit:
        def __init__(self, name):
            self.name = name
            print(self.name)

        def display(self):
            print("Hi!")
        
        def add_one(self, x:int):
            print(x + 1)
    
    print("Let's create instance of class!")    
    new = Habbit("number_1")
    print("Lets call display method of object!")
    new.display()
    print("Let's call add_one method of object!")
    new.add_one(7)
    print(f"Let's print type of our object: {type(new)}")
    print(new.name)

if __name__ == "__main__":
    main()