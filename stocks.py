import random
import os
import time
import string
import json



def start_stock(name, data):

    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

    balance = round(data[name]["balance"], 2)

    stocks = {
        "APPLE": 130.00,
        "TESLA": 83.00,
        "CONCHBANK": 22.01
    }

    # function that shows the stocks and their prices
    def stockMenu():
        print(f"APPLE: {round(stocks['APPLE'], 2)}$")
        print(f"TESLA: {round(stocks['TESLA'], 2)}$")
        print(f"CONCHBANK: {round(stocks['CONCHBANK'], 2)}$\n")
    
    # function buys stocks
    # and takes the money from the user
    # and adds the stocks to the user
    def Buy():
        clear()

        stockMenu()

        print(f"Your current balace is {balance}$")

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

        elif user_1 == "conchbank":
            if "CONCHBANK" not in data[name]["stocks"]:
                data[name]["stocks"]["CONCHBANK"] = 0
            
            data[name]["stocks"]["CONCHBANK"] += user_2
            data[name]["balance"] -= stocks["CONCHBANK"]

            with open("Users.json", "w") as file:
                json.dump(data, file, indent=4)   

    # function sells stocks and adds the money to the user
    # and removes the stocks from the user
    def Sell():
        print("At the moment you have the following stocks:\n")

        print(f"Apple: {data[name]["stocks"]["APPLE"]}")
        print(f"Tesla: {data[name]["stocks"]["TESLA"]}")
        print(f"ConchBank: {data[name]["stocks"]["CONCHBANK"]}\n")

        user_1 = input("What do you want to sell: ")
        user_2 = int(input("How many do you want to sell: "))

        if user_1 == "apple":
            if "APPLE" not in data[name]["stocks"]:
                print("You don't have this stock")
                time.sleep(2)
                return
            
            print(f"You have sold {user_2} Apple stocks for {round(stocks['APPLE'], 2)}")

            data[name]["stocks"]["APPLE"] -= user_2
            data[name]["balance"] += stocks["APPLE"]

            with open("Users.json", "w") as file:
                json.dump(data, file, indent=4)

        elif user_1 == "tesla":
            if "TESLA" not in data[name]["stocks"]:
                print("You don't have this stock")
                time.sleep(2)
                return
            
            print(f"You have sold {user_2} Tesla stocks for {round(stocks['TESLA'], 2)}")

            data[name]["stocks"]["TESLA"] -= user_2
            data[name]["balance"] += stocks["TESLA"]

            with open("Users.json", "w") as file:
                json.dump(data, file, indent=4)
        
        elif user_1 == "conchbank":
            if "CONCHBANK" not in data[name]["stocks"]:
                print("You don't have this stock")
                time.sleep(2)
                return
            
            print(f"You have sold {user_2} ConchBank stocks for {round(stocks['CONCHBANK'], 2)}")
            input("Press enter to continue....")

            data[name]["stocks"]["CONCHBANK"] -= user_2
            data[name]["balance"] += stocks["CONCHBANK"]

            with open("Users.json", "w") as file:
                json.dump(data, file, indent=4)


            

    menu = "1. Buy\n2. Sell\n3. Exit"


    # this is the main loop that runs the program
    while True:

        clear()

        print("Stock market\n")
        stockMenu()
        

        print(menu)
        
        for key in stocks:
            if stocks[key] >= 50:
                price_change = random.uniform(-20, 20)
                stocks[key] = max(0, stocks[key] + price_change)
            else:
                stocks[key] += random.randint(38, 65)


        user_input = input("> ")

        if user_input == "1":
            Buy()
        elif user_input == "2":
            Sell()
