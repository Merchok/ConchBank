import json
import os
import random
import string
import time
import hashlib
from datetime import datetime
from game1 import start_game
from stocks import start_stock

'''


 _____             _      _           _   
|     |___ ___ ___| |_   | |_ ___ ___| |_ 
|   --| . |   |  _|   |  | . | .'|   | '_|
|_____|___|_|_|___|_|_|  |___|__,|_|_|_,_|
                                          
'''

# if you see os.system func this checks the os of the user and cleares the terminal

# put the data of the json file into data var
with open("Users.json", "r") as file:
    data = json.load(file)

now = datetime.now()

# reg menu 
regMenu = "1. Sign up\n2. Sign in\n3. Exit\n"
homeMenu = "1. Make a transaction\n2. See past transactions\n3. Deposit\n4. Make Money\n "

print("=" * 30)
print("   Welcome to Conch Bank")
print("=" * 30)

# first welcome screan
print(regMenu)
welcomeChoice = input("> ")


# function that makes the transactions
def MkTransac(name):
    amount = int(input("How much to you want to transfer: "))
    Reciver = input("Enter the name of the user you want to transfer to: ")

    # gets the date of the transaction
    DateAndTime = time.strftime("%Y-%m-%d %H:%M:%S")

    # if there IS a user with that name make the transaction
    if Reciver in data:
        data[Reciver]["balance"] += amount
        data[name]["balance"] -= amount

        # send transaction info
        sendtransaction = {
            "to": Reciver,
            "amount": amount,
            "date": DateAndTime
        }

        # get transaction info
        Gettransaction = {
            "from": name,
            "amount": amount,
            "date": DateAndTime
        }
        data[name]["trans"].append(sendtransaction)
        data[Reciver]["trans"].append(Gettransaction)

        with open("Users.json", "w") as file:
            json.dump(data, file, indent=4)
        
        print("Transaction successfuly completed!")
        print(f"You have transfered {amount}$ to {Reciver}!")
    else:
        print("Sorry there is no such user :(")
        
    
# lists the transactions
def ListTrans(name):
    # walking throught the transactions one by one
    for t in data[name]["trans"]:

        # checks if the transaction was recived or sended
        if "to" in t:
            print(f"Sent {t['amount']}$ to {t['to']} on {t['date']}")
        elif "from" in t:
            print(f"Received {t['amount']}$ from {t['from']} on {t['date']}")

# home page of a user where he can pick what he wants to do with his balance and stuff
def HomePage(name):
    exit = False
    while not exit:
        balance = data[name]["balance"]

        os.system('cls' if os.name == 'nt' else 'clear')

        print(f"Hey {name}! Welcome to your home page!")
        print(f"you balance is {balance}$\n")

        print(homeMenu)
        HomeChoice = input("> ")

        if HomeChoice == "1":
            MkTransac(name)
            waitForEnter("Home page")
        elif HomeChoice == "2":
            ListTrans(name)
            waitForEnter("Home page")
        elif HomeChoice == "3":
            print("Please enter your check number: ")
            checkNum = int(input("> "))

            if checkNum == 1512:
                data[name]["balance"] += 15

                with open("Users.json", "w") as file:
                    json.dump(data, file, indent=4)
            
                print("Congrats!! Your check was successfully uploaded")
            waitForEnter("Home page")

        elif HomeChoice == "4":
            print("1. Guess the number game\n2. Stocks\n3. Exit")
            choice = input("> ")

            if choice == "1":
                start_game(name, data)
            elif choice == "2":
                start_stock(name, data)
            elif choice == "3":
                pass
            waitForEnter("Home page")
        elif HomeChoice == "5":
            print("Quitting")
            exit = True

# waits for user to press enter
def waitForEnter(pageName):
    input(f"\nPress enter to continue to {pageName}")


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
        "balance": 15,
        "trans": [],
        "stocks": ()
        }

        data[name]["transac"] = []

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
elif welcomeChoice == "3":
    pass








