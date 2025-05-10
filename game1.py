import random
import time
import os
import json
import string


# game gets name and data var
def start_game(name, data):

    # menu
    print("Welcome to Guess the number!")
    print("1. Easy\n2. Hard\n3. Exit")
    choice = input("Please choose difficulty: ")

    if choice == "1":
        num  = random.randint(1, 2)
        guess = int(input("Guess a number between 1-3: "))

        # adding changes and writes it to the file
        if guess == num:
            print("You WON! 5$ have been sended to your balance!")
            data[name]["balance"] += 5

            # writing to the file users.json
            with open("Users.json", "w") as file:
                json.dump(data, file, indent=4)
        else:
            print("You lost :(")
    
    
    elif choice == "2":
        num = random.randint(1, 10)
        guess = input("Guess a number between 1-10: ")

        if guess == num:
            print("You WON! 15$ have been sended to your balance!")
            data[name]["balance"] += 15


            with open("Users.json", "w") as file:
                json.dump(data, file, indent=4)
        else:
            print("You lost :(")

    elif choice == "3":
        pass