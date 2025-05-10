import random
import os
import time
import string
import json



def start_stock(name, data):

    stocks = {
        "APPLE": 130.00,
        "TESLA": 83.00,
        "CONCHBANK": 22.01
    }

    def stockMenu():
        print(f"APPLE: {stocks['APPLE']}$")
        print(f"TESLA: {stocks['TESLA']}$")
        print(f"CONCHBANK: {stocks['CONCHBANK']}$\n")
    
    def Buy():
        stockMenu()

        user_1 = input("What stock do you want to buy: ")
        user_2 = int(input("How many do you want to buy: "))    


        if user_1 == "apple":
            if "APPLE" not in data[name]["stocks"]:

                data[name]["stocks"]["APPLE"] = 0

            data[name]["stocks"]["APPLE"] += user_2                
            data[name]["balance"] -= stocks["APPLE"]

            with open("Users.json", "w") as file:
                json.dump(data, file, indent=4)

        elif user_1 == "tesla":
            if "TESLA" not in data[name]["stocks"]:
                data[name]["stocks"]["TESLA"] = 0
            
            data[name]["stocks"]["TESLA"] += user_2
            data[name]["balance"] -= stocks["TESLA"]

            with open("Users.json", "w") as file:
                json.dump(data, file, indent=4)
            

    menu = "1. Buy\n2. Sell\n3.Exit"



    while True:
        print("Stock market")
        print(f"APPLE: {stocks['APPLE']}$")
        print(f"TESLA: {stocks['TESLA']}$")
        print(f"CONCHBANK: {stocks['CONCHBANK']}$")
        
        print(menu)
        
        price_change = random.uniform(-5, 5)

        user_input = input("> ")

        if user_input == "1":
            Buy()
        elif user_input == "2":
            pass
