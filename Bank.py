import json
import os
import random
import string
import time
import hashlib

# if you see os.system func this checks the os of the user and cleares the terminal

# put the data of the json file into data var
with open("Users.json", "r") as file:
    data = json.load(file)

# reg menu 
regMenu = "Welcome to Conch bank\n 1. Sign up\n 2. Sign in\n 3. Exit\n"
homeMenu = "1. Make a transaction\n2. See past transactions\n3. Deposit\n4. Make Money\n "

# first welcome screan
print(regMenu)
welcomeChoice = input("> ")

# home page of a user where he can pick what he wants to do with his balance and stuff
def HomePage(name):
    balance = data[name]["balance"]

    os.system('cls' if os.name == 'nt' else 'clear')

    print(f"Hey {name}! Welcome to your home page!")
    print(f"you balance is {balance}$\n")

    print(homeMenu)
    HomeChoice = input("> ")

    if HomeChoice == "1":
        pass
    elif HomeChoice == "2":
        pass
    elif HomeChoice == "3":
        print("Please enter your check number: ")
        checkNum = int(input("> "))

        if checkNum == 1512:
            data[name]["balance"] += 15

            with open("Users.json", "w") as file:
                json.dump(data, file, indent=4)
            
            print("Congrats!! Your check was successfully uploaded")

    elif HomeChoice == "4":
        pass


# making regestration and adds to json users file
def reg():
    name = input("What is your name: ")
    password = input("Enter you new password: ")

    # encypts the password
    hashed = hashlib.sha256(password.encode()).hexdigest()

    # if there is no such user it will make a new one and add to the data file
    if name not in data:
        data[name] = {
        "password": hashed,
        "balance": 15
        }

        with open("Users.json", "w") as file:
            json.dump(data, file, indent=4)

# log in function thingy
def LogIn():
    name = input("What is your name: ")
    password = input("Enter your password: ")

    # decrypts the password
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    # if there is a user with that name and password it will log the user in. (fuck the python syntax, fuck tay)
    if name and password_hash == data[name]["password"]:
        HomePage(name)
    else:
        print("username or password are inncorect!")

# welcome screen choice
if welcomeChoice == "1":
    os.system('cls' if os.name == 'nt' else 'clear')
    reg()
elif welcomeChoice == "2":
    os.system('cls' if os.name == 'nt' else 'clear')
    LogIn()








