
# 🐚 ConchBank

> A full-featured banking system with web interface built in Python/Flask. Made in the process of learning to code :D

---

## ✨ Features

- 🔐 User Authentication
  - Account registration and login with password hashing
  - Secure session management

- 💰 Banking Functions
  - 💸 User-to-user money transfers
  - 📜 Transaction history viewing (sent and received)
  - 💳 Funds deposit system
  - 💹 Balance tracking

- 📈 Stock Trading
  - Buy and sell stocks (APPLE, TESLA, CONCHBANK)
  - Dynamic stock prices that update every minute
  - Personal portfolio management

- 🎮 Conch Combat (Clicker Game)
  - Earn coins by clicking
  - Upgrade your click power to earn more coins
  - Special "Lucky Coin" feature that provides bonus coins

- 🗄️ Data Storage
  - SQLite database for persistent data storage
  - Migration tools for legacy JSON data

- 🌐 Modern Web Interface
  - Responsive design that works on various devices
  - Clean UI with intuitive navigation

---

## 🚀 How to Run

```bash
python app.py
```

The web application will start on http://localhost:5000 by default.

---

## 🧰 Project Structure

- `app.py` - Main Flask application with all routes
- `database.py` - Database management and operations
- `conchbank.db` - SQLite database file
- `templates/` - HTML templates for web pages
- `static/` - CSS, JavaScript, and image files

---

## 🤝 Looking for Contributors

This is a fun learning project, and I'd love to have others join in!  
If you want to contribute, check the open issues or message me directly.  
All levels are welcome.

You can reach me on Discord. My username is Merchok 

---

## 🔄 Legacy Support

This project has evolved from a terminal-based application (`Bank.py`) to a full web application. If you have existing user data in `Users.json`, you can migrate it to the new SQLite database using:

```bash
python reset_and_migrate.py
```

---

## 🧠 Author

Made by Max (Merchok) 🧃  
*Learning coding :D*
