import hashlib
from flask import Flask, jsonify, render_template, request, redirect, url_for
import time
import random
import database  # Модуль для работы с базой данных SQLite


app = Flask(__name__)

# Initialize database
database.initialize_database()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        # Use SQLite authentication
        if database.authenticate_user(name, password_hash):
            return redirect(url_for("home", username=name))
        else:
            return "Wrong name or password!"

    return render_template("login.html")

@app.route("/home/<username>")
def home(username):
    user = database.get_user(username)
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

        # Create a password hash
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Check if user exists and create new user using our database function
        success = database.create_user(name, password_hash)
        
        if not success:
            return "User already exists!"

        return render_template("signup_success.html")

    
    return render_template("signup.html")


@app.route("/transfer/<username>", methods=["GET", "POST"])
def transfer(username):
    user = database.get_user(username)
    if not user:
        return "User not found"
    
    if request.method == "POST":
        receiver = request.form["receiver"]
        amount = int(request.form["amount"])
        date = time.strftime("%Y-%m-%d %H:%M:%S")

        # Check if receiver exists
        receiver_data = database.get_user(receiver)
        if not receiver_data:
            return f"User with the name {receiver} not found"
        
        # Check if sender has enough funds
        if user["balance"] < amount:
            return "Not enough money"
        
        # Update balances
        database.update_user_balance(username, user["balance"] - amount)
        database.update_user_balance(receiver, receiver_data["balance"] + amount)
        
        # Add transaction record
        database.add_transaction(username, receiver, amount, date)

        return render_template("TransferSuc.html", username=username)
    
    return render_template("transfer.html", username=username)

@app.route("/seetransfer/<username>", methods=["GET", "POST"])
def seeTransfer(username):
    # Check if user exists in database
    user = database.get_user(username)
    if not user:
        return "User not found"
    
    # Get formatted transactions from the database
    transactions = database.get_transactions_formatted(username)
        
    return render_template("seeTransfer.html", username=username, transactions=transactions)

@app.route("/deposit/<username>", methods=["GET", "POST"])
def Deposit(username):
    user = database.get_user(username)
    if not user:
        return "User with that name was not found"
    if request.method == "POST":
        DPcode = int(request.form["DPcode"])
        if DPcode == 1512:
            # Обновляем баланс в базе данных
            database.update_user_balance(username, user["balance"] + 100)
            
            # Добавляем транзакцию
            date = time.strftime("%Y-%m-%d %H:%M:%S")
            database.add_transaction("system", username, 100, date)

        return render_template("DPsucc.html", username=username)
    return render_template("Deposit.html", username=username)

last_update = 0

# 
@app.route("/stocks/<username>", methods=["GET", "POST"])
def Stocks(username):
    # Получаем информацию о пользователе из базы данных
    user = database.get_user(username)
    if not user:
        return "User with that name was not found"

    # Получаем текущие цены акций и акции пользователя
    stocks = database.get_stock_prices()
    user_stocks = database.get_user_stocks(username)
    user_balance = user["balance"]

    # Функция обновления цен акций
    def update_prices():
        for stock_name, price in stocks.items():
            if price >= 50:
                price_change = random.uniform(-20, 20)
                new_price = max(0, price + price_change)
            else:
                new_price = price + random.randint(38, 65)
                
            # Обновляем цену в базе данных
            database.update_stock_price(stock_name, new_price)

    def maybe_update_prices():
        global last_update
        now = time.time()
        if now - last_update > 60:  # раз в минуту
            update_prices()
            last_update = now
    
    def Buy(stock_name, stock_amount):
        # Рассчитываем общую стоимость
        total_price = stocks[stock_name] * stock_amount
        
        # Проверяем, достаточно ли денег
        if user_balance < total_price:
            return "Sorry you not have enough money to be able to buy stocks!"
        else:
            # Обновляем баланс пользователя
            database.update_user_balance(username, user_balance - total_price)
            
            # Обновляем количество акций
            current_amount = user_stocks.get(stock_name, 0)
            database.update_user_stock(username, stock_name, current_amount + stock_amount)

    def Sell(stock_name, stock_amount):
        # Получаем текущее количество акций
        current_amount = user_stocks.get(stock_name, 0)
        
        # Проверяем, достаточно ли акций
        if current_amount >= stock_amount:
            # Обновляем баланс пользователя
            sell_price = stocks[stock_name] * stock_amount
            database.update_user_balance(username, user_balance + sell_price)
            
            # Обновляем количество акций
            database.update_user_stock(username, stock_name, current_amount - stock_amount)
        else:
            return "You don't have enough of this stock"

    if request.method == "POST":
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
    
    # Возвращаем шаблон с актуальными данными
    return render_template("stocks.html", 
                          username=username,
                          stocks=stocks,
                          user_stocks=user_stocks,
                          balance=user_balance)

@app.route("/clicker/<username>")
def clicker(username):
    user = database.get_user(username)

    if not user:
        return "User not found"
    
    return render_template("clicker.html", username=username)

@app.route("/click/<username>", methods=["POST"])
def click(username):
    user = database.get_user(username)

    if not user:
        return jsonify({"error": "user not found"})
    
    # Получаем данные кликера
    clicker_data = database.get_clicker_data(username)
    
    # Добавляем монеты
    new_coins = clicker_data["coins"] + clicker_data["click_power"]
    
    # Обновляем в базе данных
    database.update_clicker_data(username, new_coins, clicker_data["click_power"])

    return jsonify({"coins": new_coins})

@app.route("/get_coins/<username>", methods=["GET"])
def get_coinds(username):
    user = database.get_user(username)

    if not user:
        return jsonify({"error": "user not found"})
    
    # Получаем данные кликера
    clicker_data = database.get_clicker_data(username)
    
    return jsonify({
        "coins": clicker_data["coins"],
        "click_power": clicker_data["click_power"]
    })

@app.route("/upgrade/<username>", methods=["POST"])
def upgrade(username):
    user = database.get_user(username)

    if not user:
        return jsonify({"error": "User not found"})
    
    # Получаем данные кликера
    clicker_data = database.get_clicker_data(username)
    
    # Стоимость улучшения
    price = 2000
    
    if clicker_data["coins"] >= price:
        # Обновляем данные кликера
        database.update_clicker_data(
            username,
            clicker_data["coins"] - price,
            clicker_data["click_power"] + 1
        )
        
        # Получаем обновленные данные
        updated_data = database.get_clicker_data(username)
        
        return jsonify({
            "success": True,
            "coins": updated_data["coins"],
            "click_power": updated_data["click_power"]
        })
    else:
        return jsonify({"error": "Not enough coins"})

    

if __name__ == "__main__":
    app.run(debug=True)
