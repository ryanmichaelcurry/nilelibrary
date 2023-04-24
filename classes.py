import sqlite3

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
 
    def login(self):
        pass

    def signout(self):
        pass

    def signup(self):
        pass

    def getStatus(self):
        pass

    def setStatus(self):
        pass

    def getUsername(username):

        return None

    def getID(self):
        pass


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
        for item in self.items:
            print(f"x{item['amount']}) {item['name']} ------- ${item['price']}")


class Shop:
    def __init__(self):
        self.items = []

    def load_items_from_database(self):
        conn = sqlite3.connect('shop.db')
        c = conn.cursor()
        c.execute("SELECT name, amount, price FROM items")
        results = c.fetchall()
        conn.close()

        self.items = [{'name': row[0], 'amount': row[1], 'price': row[2]} for row in results]

    def view_items(self):
        self.load_items_from_database()
        for item in self.items:
            print(f"{item['name']} ------- ${item['price']}")
