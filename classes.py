import sqlite3
import bcrypt

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
        self.isLogin = False
 
    def login(self):
        conn = sqlite3.connect('shop.db')
        c = conn.cursor()

        c.execute('''
        CREATE TABLE IF NOT EXISTS
            `user` (
                `user_id` INTEGER PRIMARY KEY,
                `username` varchar(255) not null,
                `password` varchar(255) not null,
                `status` tinyint not null
            )
        ''')

        c.execute("SELECT * FROM user WHERE username = ?", (self.username))
        results = c.fetchall()

        if results[0][3] <= 0: # status is non-positive
            pass

        hashed = results[0][2]

        if bcrypt.checkpw(self.password, hashed):
            self.isLogin = True
        else:
            print("Incorrect Credentials")

        pass

    def signout(self):
        self.isLogin = False
        pass

    def signup(self):
        conn = sqlite3.connect('shop.db')
        c = conn.cursor()

        c.execute('''
        CREATE TABLE IF NOT EXISTS
            `user` (
                `user_id` INTEGER PRIMARY KEY,
                `username` varchar(255) not null,
                `password` varchar(255) not null,
                `status` tinyint not null
            )
        ''')

        c.execute("SELECT username FROM user WHERE username = ?", (self.username))
        results = c.fetchall()

        if not results:
            hashed = bcrypt.hashpw(self.password, bcrypt.gensalt())
            c.execute("INSERT INTO items (username, password, status) VALUES (?, ?, ?)",
                    (self.username, hashed, 1))
            conn.commit()
        
        conn.close()
        pass

    def getStatus(self):
        conn = sqlite3.connect('shop.db')
        c = conn.cursor()

        c.execute('''
        CREATE TABLE IF NOT EXISTS
            `user` (
                `user_id` INTEGER PRIMARY KEY,
                `username` varchar(255) not null,
                `password` varchar(255) not null,
                `status` tinyint not null
            )
        ''')

        c.execute("SELECT user_id, username, password, status FROM user WHERE username = ?", (self.username))
        results = c.fetchall()

        return results[0][1]

    def setStatus(self):
        pass

    def getUsername(username):
        return None

    def getID(self):
        return self.id


class Cart:
    def __init__(self):
        self.productID = None
        self.CategoryID = None

    def goBack(self):
        pass

    def viewCart(self):
        pass

    def remove(self):
        pass

    def shipping(self):
        pass

    def quantity(self):
        pass

# This is where the all the items will sit but the shop class is where the customer will be able to view the items and add them to the cart
class Item:
    def __init__(self):
        self.name = None
        self.amount = 0
        self.price = 0.00

    def setName(self, name):
        self.name = name

    def setAmount(self, amount):
        self.amount = amount

    def subtractAmount(self, amount):
        self.amount -= amount

    def setPrice(self, price):
        self.price = price

    def getName(self):
        return self.name

    def getAmount(self):
        return self.amount

    def getPrice(self):
        return self.price

    def save_to_database(self):
        conn = sqlite3.connect('shop.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS items
                    (name TEXT PRIMARY KEY, amount INTEGER, price REAL)''')
        c.execute("INSERT OR REPLACE INTO items (name, amount, price) VALUES (?, ?, ?)",
                  (self.name, self.amount, self.price))
        conn.commit()
        conn.close()
    
    def load_items_from_database(self):
        conn = sqlite3.connect('shop.db')
        c = conn.cursor()
        c.execute("SELECT name, amount, price FROM items")
        results = c.fetchall()
        conn.close()

        self.items = [{'name': row[0], 'amount': row[1], 'price': row[2]} for row in results]

    def view_items(self):
        self.load_items_from_database()
        if not self.items:
            print("\nSorry the shop is currently empty! Please Try again later.")
            return
        
        for item in self.items:
            print(f"(x{item['amount']}) {item['name']} ------- ${item['price']:.2f}")
    
    def delete_item(self, item_name):
        conn = sqlite3.connect('shop.db')
        c = conn.cursor()
        c.execute("DELETE FROM items WHERE name=?", (item_name,))
        conn.commit()
        conn.close()
        print(f"'{item_name}' has been deleted from our inventory.")


class Shop:
    def __init__(self):
        conn = sqlite3.connect('shop.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS items
                     (name TEXT PRIMARY KEY, price REAL, amount INTEGER)''')
        conn.commit()
        conn.close()

    def load_database(self):
        conn = sqlite3.connect('shop.db')
        c = conn.cursor()
        c.execute("SELECT name, price, amount FROM items")
        results = c.fetchall()
        conn.close()

        if not results:
            print("Sorry the shop is empty! Please try again later!")  
            return True 

        print("Items in the shop:")
        for row in results:
            name, price, amount = row
            print(f"(x{item['amount']}) {item['name']} ------- ${item['price']:.2f}")
        return False 

