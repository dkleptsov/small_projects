from random import randint

def main():
    class Toolbox:
        @staticmethod
        def add5(x):
            return x+5
        
    
    
    class Habbit:
        def __init__(self, name:str, description:str="Empty"):
            self.name = name
            self.description = description
            self.days = randint(0,100)
            print(f"Habbit with the name {self.name} successfully created!")
            
        # Use only if you need different outputs for print(x) and print([x])
        # def __str__(self):
        #     return self.name

        def __repr__(self):
            return self.name
        
        def display(self):
            print("Hi!")
        
        def add_one(self, x:int):
            print(x + 1)
            
        def get_days(self):
            return self.days
    
    class User:
        number_of_users = 0
        def __init__(self, name):
            self.name = name
            self.habbits = []
            self.is_active = False
            User.number_of_users += 1
    
    
        def add_habbit(self, habbit):
            self.habbits.append(habbit)
            return True
        
        def get_average_days(self):
            value = 0
            for habbit in self.habbits:
                value += habbit.get_days()
            value /= len(self.habbits)
            return value
        
        @classmethod
        def get_number_of_users(cls):
            return cls.number_of_users
        
    class Owner(User):
        def __init__(self, name, surname):
            super().__init__(name)
            self.surname = surname
        
        def print_habbits(self):
            for habbit in self.habbits:
                print(habbit)
            
    print("Let's create instance of class!")    
    h1 = Habbit("number_1")
    
    print("Lets call display method of object!")
    h1.display()
    
    print("Let's call add_one method of object!")
    h1.add_one(7)
    
    print(f"Let's print type of our object: {type(h1)}")
    
    print(f"Let's print attributes of our object: name - {h1.name}, description - {h1.description}")
    print(h1.name)
    
    print("Let's create user with multiple habbits!")
    h2 = Habbit("number_2")
    h3 = Habbit("number_3")
    h4 = Habbit("number_4")
    h5 = Habbit("number_5")
    
    u1 = User("user_1")
    for i in [h1, h2, h3, h4, h5]:
        u1.add_habbit(i)
    
    print(u1.habbits[0])
    
    print(f"Average number of days for all habbits of user: {u1.get_average_days()}")

    print("Let's create inheritance!")
    o1 = Owner("owner_1", "surname_1")
    for i in [h1, h2, h3, h4, h5]:
        o1.add_habbit(i)
    # new method
    o1.print_habbits()

    #new attribute
    print(f"New attribute of instance: {o1.surname}")
    
    print("Let's explore class attributes!")
    o1.number_of_users = 16
    print(f"Total number of users: {User.number_of_users}")
    print(f"Total number of users: {o1.number_of_users}")
    
    print(Owner.get_number_of_users())
    
    print ("Let's demonstarte static methods!")
    print(Toolbox.add5(9))
    
if __name__ == "__main__":
    main()