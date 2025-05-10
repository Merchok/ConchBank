import random
import os
import time
import string



def start_stock(name, data):

    stocks = {
        "APPLE": 130.00,
        "TESLA": 83.00,
        "CONCHBANK": 22.01
    }

    def stockMenu():
        print(f"APPLE: {stocks["APPLE"]}$")
        print(f"TESLA: {stocks["TESLA"]}$")
        print(f"CONCHBANK: {stocks["CONCHBANK"]}$\n")
    
    def Buy():
        stockMenu()

        user_1 = input("What stock do you want to buy: ")
        user_2 = input("How many do you want to buy: ")    


        if user_1 == "apple":
            pass
            

    menu = "1. Buy\n2. Sell\n3.Exit"


    price_change = random.uniform(-5, 5)

    while True:
        print("Stock market")
        print(f"APPLE: {stocks["APPLE"]}$")
        print(f"TESLA: {stocks["TESLA"]}$")
        print(f"CONCHBANK: {stocks["CONCHBANK"]}$")
        
        print(menu)
        

        user_input = input("> ")

        if user_input == "1":
            pass
        elif user_input == "2":
            pass
