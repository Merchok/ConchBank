import sqlite3
import json
import os
import time
import random

def get_db_connection():
    """Create a connection to the SQLite database"""
    conn = sqlite3.connect('conchbank.db')
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
    return conn

def initialize_database(force_recreate=False):
    """Create tables if they don't exist or if force_recreate is True"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Проверяем существуют ли таблицы
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    tables_exist = cursor.fetchone() is not None
    
    # Если таблицы не существуют или нужно пересоздать, создаем их
    if not tables_exist or force_recreate:
        # Если таблицы существуют и нужно пересоздать, удаляем их
        if force_recreate and tables_exist:
            cursor.execute("DROP TABLE IF EXISTS transactions")
            cursor.execute("DROP TABLE IF EXISTS user_stocks")
            cursor.execute("DROP TABLE IF EXISTS clicker")
            cursor.execute("DROP TABLE IF EXISTS stocks")
            cursor.execute("DROP TABLE IF EXISTS users")        # Create users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            balance REAL NOT NULL,
            lucky_coin_upgrade INTEGER DEFAULT 0
        )
        ''')
    
    # Create stocks table for stock prices
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS stocks (
        name TEXT PRIMARY KEY,
        price REAL NOT NULL
    )
    ''')
    
    # Create user_stocks table to track user's stocks
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_stocks (
        username TEXT,
        stock_name TEXT,
        amount INTEGER NOT NULL,
        PRIMARY KEY (username, stock_name),
        FOREIGN KEY (username) REFERENCES users(username),
        FOREIGN KEY (stock_name) REFERENCES stocks(name)
    )
    ''')
    
    # Create transactions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        from_user TEXT,
        to_user TEXT,
        amount REAL NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY (from_user) REFERENCES users(username),
        FOREIGN KEY (to_user) REFERENCES users(username)
    )
    ''')
    
    # Create clicker table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clicker (
        username TEXT PRIMARY KEY,
        coins INTEGER NOT NULL,
        click_power INTEGER NOT NULL,
        FOREIGN KEY (username) REFERENCES users(username)
    )
    ''')
    
    conn.commit()
    conn.close()

def migrate_data_from_json():
    """Migrate data from JSON files to SQLite database"""
    if not os.path.exists('Users.json') or not os.path.exists('Stocks.json'):
        print("JSON files not found")
        return False
    
    # Load JSON data
    with open('Users.json', 'r') as f:
        users_data = json.load(f)
    
    with open('Stocks.json', 'r') as f:
        stocks_data = json.load(f)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Insert stock prices
        for stock_name, price in stocks_data.items():
            cursor.execute('INSERT OR REPLACE INTO stocks VALUES (?, ?)', 
                        (stock_name, price))
        
        # Insert users and their data
        for username, user_data in users_data.items():
            # Insert user
            cursor.execute('INSERT OR REPLACE INTO users VALUES (?, ?, ?)',
                        (username, user_data['password'], user_data['balance']))
            
            # Insert user stocks
            for stock_name, amount in user_data['stocks'].items():
                cursor.execute('INSERT OR REPLACE INTO user_stocks VALUES (?, ?, ?)',
                            (username, stock_name, amount))
            
            # Insert clicker data
            cursor.execute('INSERT OR REPLACE INTO clicker VALUES (?, ?, ?)',
                        (username, user_data['clicker']['coins'], 
                        user_data['clicker']['click_power']))
            
            # Insert transactions
            for transaction in user_data['trans']:
                if 'from' in transaction:
                    # Received money
                    cursor.execute(
                        'INSERT INTO transactions (from_user, to_user, amount, date) VALUES (?, ?, ?, ?)',
                        (transaction['from'], username, transaction['amount'], transaction['date'])
                    )
                elif 'to' in transaction:
                    # Sent money
                    cursor.execute(
                        'INSERT INTO transactions (from_user, to_user, amount, date) VALUES (?, ?, ?, ?)',
                        (username, transaction['to'], transaction['amount'], transaction['date'])
                    )
        
        conn.commit()
        print("Migration completed successfully")
        return True
    except Exception as e:
        print(f"Error during migration: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

# Helper functions for app.py

def get_user(username):
    """Get user data from database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get user basic info
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    
    if user is None:
        conn.close()
        return None
    
    # Get user stocks
    cursor.execute('''
        SELECT stock_name, amount FROM user_stocks 
        WHERE username = ?
    ''', (username,))
    stocks = {row['stock_name']: row['amount'] for row in cursor.fetchall()}
    
    # Get clicker data
    cursor.execute('SELECT * FROM clicker WHERE username = ?', (username,))
    clicker = cursor.fetchone()
    
    # Build user object similar to JSON structure
    user_data = {
        'password': user['password'],
        'balance': user['balance'],
        'trans': get_transactions_raw(username, conn),  # We need the full transaction objects
        'stocks': stocks if stocks else {
            "APPLE": 0,
            "TESLA": 0,
            "CONCHBANK": 0
        },
        'clicker': {
            'coins': clicker['coins'] if clicker else 0,
            'click_power': clicker['click_power'] if clicker else 1
        }
    }
    
    conn.close()
    return user_data

def authenticate_user(username, password_hash):
    """Check if username and password hash match"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    
    conn.close()
    
    if user and user['password'] == password_hash:
        return True
    return False

def get_transactions_raw(username, connection=None):
    """Get raw transaction data for a user"""
    close_conn = False
    if connection is None:
        connection = get_db_connection()
        close_conn = True
        
    cursor = connection.cursor()
    
    cursor.execute('''
        SELECT * FROM transactions 
        WHERE from_user = ? OR to_user = ?
        ORDER BY date DESC
    ''', (username, username))
    
    transactions = cursor.fetchall()
    
    # Format transactions similar to JSON structure
    formatted_transactions = []
    for t in transactions:
        if t['from_user'] == username:
            # Sent money
            formatted_transactions.append({
                'to': t['to_user'],
                'amount': t['amount'],
                'date': t['date']
            })
        else:
            # Received money
            formatted_transactions.append({
                'from': t['from_user'],
                'amount': t['amount'],
                'date': t['date']
            })
    
    if close_conn:
        connection.close()
        
    return formatted_transactions

def get_transactions_formatted(username):
    """Get formatted transaction strings for a user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM transactions 
        WHERE from_user = ? OR to_user = ?
        ORDER BY date DESC
    ''', (username, username))
    
    transactions = cursor.fetchall()
    conn.close()
    
    # Format transactions as strings for display
    formatted_transactions = []
    for t in transactions:
        if t['from_user'] == username:
            formatted_transactions.append(
                f"Sent {t['amount']}$ to {t['to_user']} on {t['date']}"
            )
        else:
            formatted_transactions.append(
                f"Received {t['amount']}$ from {t['from_user']} on {t['date']}"
            )
    
    return formatted_transactions

def update_user_balance(username, new_balance):
    """Update user balance in the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('UPDATE users SET balance = ? WHERE username = ?', 
                  (new_balance, username))
    
    conn.commit()
    conn.close()

def add_transaction(from_user, to_user, amount, date):
    """Add a new transaction to the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        'INSERT INTO transactions (from_user, to_user, amount, date) VALUES (?, ?, ?, ?)',
        (from_user, to_user, amount, date)
    )
    
    conn.commit()
    conn.close()
    
def get_stock_prices():
    """Get all stock prices"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT name, price FROM stocks')
    stocks = {row['name']: row['price'] for row in cursor.fetchall()}
    
    conn.close()
    return stocks

def update_stock_price(name, price):
    """Update stock price"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('UPDATE stocks SET price = ? WHERE name = ?', (price, name))
    
    conn.commit()
    conn.close()

def update_all_stock_prices():
    """Update all stock prices randomly"""
    stocks = get_stock_prices()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    for name, price in stocks.items():
        if price >= 50:
            price_change = (price * random.uniform(-0.2, 0.2))  # -20% to +20%
            new_price = max(0, price + price_change)
        else:
            new_price = price + random.randint(38, 65)
            
        cursor.execute('UPDATE stocks SET price = ? WHERE name = ?', 
                      (new_price, name))
    
    conn.commit()
    conn.close()
    
def get_user_stocks(username):
    """Get user's stock holdings"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT stock_name, amount FROM user_stocks 
        WHERE username = ?
    ''', (username,))
    
    stocks = {row['stock_name']: row['amount'] for row in cursor.fetchall()}
    
    conn.close()
    return stocks

def update_user_stock(username, stock_name, amount):
    """Update user's stock holdings"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT OR REPLACE INTO user_stocks (username, stock_name, amount)
        VALUES (?, ?, ?)
    ''', (username, stock_name, amount))
    
    conn.commit()
    conn.close()

def get_clicker_data(username):
    """Get user's clicker data"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT coins, click_power FROM clicker WHERE username = ?', 
                  (username,))
    
    clicker = cursor.fetchone()
    conn.close()
    
    if clicker:
        return {'coins': clicker['coins'], 'click_power': clicker['click_power']}
    else:
        return {'coins': 0, 'click_power': 1}

def update_clicker_data(username, coins, click_power):
    """Update user's clicker data"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT OR REPLACE INTO clicker (username, coins, click_power)
        VALUES (?, ?, ?)
    ''', (username, coins, click_power))
    
    conn.commit()
    conn.close()

def create_user(username, password_hash):
    """Create a new user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if user already exists
        cursor.execute('SELECT username FROM users WHERE username = ?', (username,))
        if cursor.fetchone():
            conn.close()
            return False
          # Insert user with starting balance
        cursor.execute('INSERT INTO users VALUES (?, ?, ?, ?)', 
                    (username, password_hash, 15.0, 0))
        
        # Insert default stocks (0 quantity for each)
        stock_names = ['APPLE', 'TESLA', 'CONCHBANK']
        for stock in stock_names:
            cursor.execute('INSERT INTO user_stocks VALUES (?, ?, ?)', 
                        (username, stock, 0))
        
        # Insert default clicker data
        cursor.execute('INSERT INTO clicker VALUES (?, ?, ?)', 
                    (username, 0, 1))
        
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Error creating user: {e}")
        return False
    finally:
        conn.close()

def set_lucky_coin_upgrade(username):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT lucky_coin_upgrade FROM users WHERE username = ?",
        (username,)
    )

    row = cursor.fetchone()

    if row and row['lucky_coin_upgrade'] == 0:
        cursor.execute(
            "UPDATE users SET lucky_coin_upgrade = 1 WHERE username = ?",
            (username,)
        )
        conn.commit()
        result = True
    else:
        result = False
    
    conn.close()
    return result

def get_lucky_coin_last_time(username):
    conn = get_db_connection()
    cursor = conn.cursor()

    user = get_user(username)

    now = time.time()
    last_time = 0

    cursor.execute(
        "SELECT lucky_coin_last_time FROM users WHERE username = ?",
            (username,)
    )
    row = cursor.fetchone()
    conn.close()

    if row and row[0]:
        return int(row[0])
    else:
        return 0
    
def Lucky_coin_time(username, timestamp):
    conn = get_db_connection()
    cursor = conn.cursor()

    user = get_user(username)
    
    cursor.execute(
        "UPDATE users SET lucky_coin_last_time = ? WHERE username = ?",
        (timestamp, username)
    )

    conn.commit()
    conn.close()

def has_lucky_coin_upgrade(username):
    conn = get_db_connection()
    cursor = conn.cursor()

    user = get_user(username)

    cursor.execute(
        "SELECT lucky_coin_upgrade FROM users WHERE username = ?",
        (username,)
    )

    row = cursor.fetchone()
    conn.close()
    return row and row[0] == 1

# leaderboard
def get_leaderboard(limit=10):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT username, coins
        FROM clicker
        ORDER BY coins DESC
        LIMIT ?
        """, (limit,))
    
    results = cursor.fetchall()

    leaders = []
    for row in results:
        leaders.append({
            'username': row['username'],
            'coins': row['coins']
        })
    
    conn.close()
    return leaders

# Run initialization when the module is imported
if __name__ == "__main__":
    initialize_database()
    migrate_data_from_json()