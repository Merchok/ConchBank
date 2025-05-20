import flask
import json
import hashlib
from flask import Flask, jsonify, render_template, request, redirect, url_for
import time
import random


app = Flask(__name__)

with open("Users.json", "r") as f:
    users = json.load(f)

with open("Stocks.json", "r") as s:
    stockss = json.load(s)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        if name in users and users[name]["password"] == password_hash:
            return redirect(url_for("home", username=name))
        else:
            return "Wrong name or password!"

    return render_template("login.html")

@app.route("/home/<username>")
def home(username):
    user = users.get(username)
    if user:
        balance = user["balance"]
        return render_template("home.html", username=username, balance=round(balance, 2))
    else:
        return "User not found."
    
@app.route("/signup_success")
def signup_success():
    return render_template("signup_success.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]


        if name in users:
            return "User already exist!"

        password_hash = hashlib.sha256(password.encode()).hexdigest()

        users[name] = {
            "password": password_hash,
            "balance": 15,
            "trans": [],
            "stocks": {
                "APPLE": 0,
                "TESLA": 0,
                "CONCHBANK": 0
            },
            "clicker": {
            "coins": 0,
            "click_power": 1
            }
        }

        with open("Users.json", "w") as f:
            json.dump(users, f, indent=4)

        return render_template("signup_success.html")

    
    return render_template("signup.html")


@app.route("/transfer/<username>", methods=["GET", "POST"])
def transfer(username):
    user = users.get(username)
    if not user:
        return "User not found"
    
    if request.method == "POST":
        reciver = request.form["receiver"]
        amount = int(request.form["amount"])
        date = time.strftime("%Y-%m-%d %H:%M:%S")

        if reciver not in users:
            return f"User with the name {reciver} not found"
        
        if users[username]["balance"] < amount:
            return "Not enough money"
        
                # send transaction info
        sendtransaction = {
            "to": reciver,
            "amount": amount,
            "date": date        
        }

        # get transaction info
        Gettransaction = {
            "from": username,
            "amount": amount,
            "date": date
        }

        users[username]["balance"] -= amount
        users[reciver]["balance"] += amount
        users[username]["trans"].append(sendtransaction)
        users[reciver]["trans"].append(Gettransaction)

        with open("Users.json", "w") as f:
            json.dump(users, f, indent=4)

        return render_template("TransferSuc.html", username=username)
    
    return render_template("transfer.html", username=username)

@app.route("/seetransfer/<username>", methods=["GET", "POST"])
def seeTransfer(username):
    user = users.get(username)
    if not user:
        return "User not found"
    
    transactions = []
    
    for t in users[username]["trans"]:

        if "to" in t:
            transactions.append(f"Sent {t['amount']}$ to {t['to']} on {t['date']}")
        elif "from" in t:
            transactions.append(f"Received {t['amount']}$ from {t['from']} on {t['date']}")
        
        
    return render_template("seeTransfer.html", username=username, transactions=transactions)

@app.route("/deposit/<username>", methods=["GET", "POST"])
def Deposit(username):
    user = users.get(username)
    if not user:
        return "User with that name was not found"
    if request.method == "POST":
        DPcode = int(request.form["DPcode"])
        if DPcode == 1512:
            users[username]["balance"] += 100

        with open("Users.json", "w") as f:
            json.dump(users, f, indent=4)

        return render_template("DPsucc.html", username=username)
    return render_template("Deposit.html", username=username)

last_update = 0

# 
@app.route("/stocks/<username>", methods=["GET", "POST"])
def Stocks(username):
    user = users.get(username)
    if not user:
        return "User with that name was not found"

    stocks = stockss
    user_balance = users[username]["balance"]

    # function to update stock prices 
    def update_prices():
        for key in stocks:
            if stocks[key] >= 50:
                price_change = random.uniform(-20, 20)
                stocks[key] = max(0, stocks[key] + price_change)

                with open("Stocks.json", "w") as s:
                    json.dump(stockss, s, indent=4)
            else:
                stocks[key] += random.randint(38, 65)

                with open("Stocks.json", "w") as s:
                    json.dump(stockss, s, indent=4)

    def  maybe_update_prices():
        global last_update
        now = time.time()
        if now - last_update > 60:  # раз в минуту
            update_prices()
            last_update = now
    
    def Buy(stock_name, stock_amount):

        totalPrice = stocks[stock_name] * stock_amount
        if user_balance < totalPrice:
            return "Sorry you not have enough money to be able to buy stocks!"
        else:
            if stock_name == "APPLE":
                users[username]["balance"] -= stocks[stock_name] * stock_amount
                users[username]["stocks"]["APPLE"] += stock_amount

            elif stock_name =="TESLA":
                users[username]["balance"] -= stocks[stock_name] * stock_amount
                users[username]["stocks"]["TESLA"] += stock_amount
            
            elif stock_name == "CONCHBANK":
                users[username]["balance"] -= stocks[stock_name] * stock_amount
                users[username]["stocks"]["CONCHBANK"] += stock_amount
            
            with open("Users.json", "w") as f:
                json.dump(users, f, indent=4)

    def Sell(stock_name, stock_amount):
        if stock_name == "APPLE" and users[username]["stocks"]["APPLE"] >= stock_amount:
            users[username]["stocks"]["APPLE"] -= stock_amount
            users[username]["balance"] += stocks["APPLE"] * stock_amount

        elif stock_name == "TESLA" and users[username]["stocks"]["TESLA"] >= stock_amount:
            users[username]["stocks"]["TESLA"] -= stock_amount
            users[username]["balance"] += stocks["TESLA"] * stock_amount

        elif stock_name == "CONCHBANK" and users[username]["stocks"]["CONCHBANK"] >= stock_amount:
            users[username]["stocks"]["CONCHBANK"] -= stock_amount
            users[username]["balance"] += stocks["CONCHBANK"] * stock_amount
        else:
            return "You don't have this stock"

        
        with open("Users.json", "w") as f:
            json.dump(users, f, indent=4)

    if request.method == "POST":
        user = users.get(username)
        stock_name = request.form['stock_name']
        stock_amount = int(request.form['stock_amount'])
        action = request.form['action']

        if action == "buy":
            result = Buy(stock_name, stock_amount)
            if result:
                return result

        elif action == "sell":
            result = Sell(stock_name, stock_amount)
            if result:
                return result

        maybe_update_prices()
        return redirect(url_for('Stocks', username=username))
    
    # Добавьте в самом конце функции Stocks():
    return render_template("stocks.html", 
                            username=username,
                            stocks=stocks,
                            user_stocks=users[username]["stocks"],
                            balance=users[username]["balance"])

@app.route("/clicker/<username>")
def clicker(username):
    user = users.get(username)

    if not user:
        return "User not found"
    
    return render_template("clicker.html", username=username)

@app.route("/click/<username>", methods=["POST"])
def click(username):
    user = users.get(username)

    if not user:
        return jsonify({"error": "user not found"})
    
    coins = user['clicker']['coins']

    user["clicker"]["coins"] += user["clicker"]["click_power"] # adds coins on click with the power the user have

    with open("Users.json", "w") as f:
        json.dump(users, f, indent=4)

    return jsonify({"coins": user["clicker"]["coins"]})



@app.route("/get_coins/<username>", methods=["GET"])
def get_coinds(username):
    user = users.get(username)

    if not user:
        return jsonify({"error": "user not found"})
    
    return jsonify({
        "coins": user["clicker"]["coins"],
        "click_power": user["clicker"]["click_power"]
    })

@app.route("/upgrade/<username>", methods=["POST"])
def upgrade(username):
    user = users.get(username)

    if not user:
        return jsonify({"error": "User not found"})
    
    def buy_click_power_upgrade():
        price = 2000

        if user["clicker"]["coins"] >= price:

            user["clicker"]["coins"] -= price
            user["clicker"]["click_power"] += 1

            with open("Users.json", "w") as f:
                json.dump(users, f, indent=4)
        else:
            return jsonify({"error": "Not enough coins"})

    

if __name__ == "__main__":
    app.run(debug=True)
