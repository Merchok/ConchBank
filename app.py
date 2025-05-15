import flask
import json
import hashlib
from flask import Flask, render_template, request, redirect, url_for
import time


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
            return "Wrong name or password!"

    return render_template("login.html")

@app.route("/home/<username>")
def home(username):
    user = users.get(username)
    if user:
        balance = user["balance"]
        return render_template("home.html", name=username, balance=round(balance, 2))
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
            "stocks": {}
        }

        with open("Users.json", "w") as f:
            json.dump(users, f, indent=4)

        return render_template("signup_success.html")

    
    return render_template("signup.html")


if __name__ == "__main__":
    app.run(debug=True)
