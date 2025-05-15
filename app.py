import flask
import json
import hashlib
from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)

with open("Users.json", "r") as f:
    users = json.load(f)

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
            return "Неверное имя или пароль!"

    return render_template("login.html")

@app.route("/home/<username>")
def home(username):
    user = users.get(username)
    if user:
        balance = user["balance"]
        return render_template("home.html", name=username, balance=round(balance, 2))
    else:
        return "Пользователь не найден."


if __name__ == "__main__":
    app.run(debug=True)
