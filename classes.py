import sqlite3
import bcrypt

class User:
    def __init__(self, username, password):
        self.id = -1
        self.username = username
        self.password = password
        self.status = -1
        self.address = ""
        self.credit_card = ""
 
    def login(self):
        conn = sqlite3.connect('shop.db')
        c = conn.cursor()

        c.execute('''
        CREATE TABLE IF NOT EXISTS
            `user` (
                `user_id` INTEGER PRIMARY KEY,
                `username` varchar(255) not null,
                `password` varchar(255) not null,
                `address` varchar (255),
                `credit_card` varchar(255),
                `status` tinyint not null
            )
        ''')

        c.execute("SELECT * FROM user WHERE username = ?", (self.username,))
        results = c.fetchall()

        if len(results) <= 0:
            return False

        if results[0][5] <= 0: # status is non-positive
            return False

        self.id = results[0][0]

        self.address = results[0][3]
        self.credit_card = results[0][4]
        self.status = results[0][5]

        hashed = results[0][2]

        if bcrypt.checkpw(self.password.encode('utf-8'), hashed):
            return True

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
                `address` varchar (255),
                `credit_card` varchar(255),
                `status` tinyint not null
            )
        ''')

        c.execute("SELECT username FROM user WHERE username = ?", (self.username,))
        results = c.fetchall()

        if len(results) <= 0:   # user does not exist
            hashed = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())
            c.execute("INSERT INTO user (username, password, status) VALUES (?, ?, ?)",
                    (self.username, hashed, 1))
            conn.commit()
            conn.close()
            return True
        
        else:
            return False
        

    def setAddress(self, address):
        if self.id <= 0:
            return False
        
        conn = sqlite3.connect('shop.db')
        c = conn.cursor()
        c.execute("UPDATE user SET address = ? WHERE user_id = ?", (address, self.id))
        conn.commit()
        conn.close()
        return True
    
    def setCreditCard(self, credit_card):
        if self.id <= 0:
            return False

        conn = sqlite3.connect('shop.db')
        c = conn.cursor()
        c.execute("UPDATE user SET credit_card = ? WHERE user_id = ?", (credit_card, self.id))
        conn.commit()
        conn.close()
        return True

    def getOrderHistory(self):
        conn = sqlite3.connect('shop.db')
        c = conn.cursor()

        c.execute('''
        CREATE TABLE IF NOT EXISTS
            `cart` (
                `cart_id` INTEGER PRIMARY KEY,
                `user_id` INTEGER not null,
                `checkout` tinyint not null
            )
        ''')

        c.execute('''
        CREATE TABLE IF NOT EXISTS
            `cart_item` (
                `cart_item_id` INTEGER PRIMARY KEY,
                `cart_id` INTEGER not null,
                `item_id` INTEGER not null,
                `amount` INTEGER not null
            )
        ''')

        c.execute("SELECT cart_id FROM cart WHERE user_id = ? AND checkout = ?", (self.id, 1))
        results = c.fetchall()

        if len(results) <= 0:
            print("\nThere is no order history!")
            return True


        for cart in results:

            total = 0
            c.execute("SELECT item_id, amount FROM cart_item WHERE cart_id = ?", (cart[0],))
            newResults = c.fetchall()
            
            for item in newResults:
                item_id, quantity = item
                c.execute("SELECT price FROM items WHERE item_id = ?", (item_id,))
                newNewResults = c.fetchall()
                total += newNewResults[0][0] * quantity
        
            print(f"Order ID #{cart[0]}: ------- ${total:.2f}")
        
        return True
    
    def deleteAccount(self):
        conn = sqlite3.connect('shop.db')
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS items
                    (item_id INTEGER PRIMARY KEY, user_id INTEGER not null, name varchar(255) not null, amount INTEGER not null, price REAL not null)''')
        
        # Delete user's inventory (if they are seller, if just buyer, nothing will happen)
        c.execute("DELETE FROM items WHERE user_id = ?", (self.id,))
        conn.commit()

        c.execute("DELETE FROM user WHERE user_id = ?", (self.id,))
        conn.commit()

        conn.close()
        return True

    def getStatus(self):
        return self.status

    def setStatus(self, status: int):
        if self.id <= 0:
            return False

        conn = sqlite3.connect('shop.db')
        c = conn.cursor()
        c.execute("UPDATE user SET status = ? WHERE user_id = ?", (status, self.id))
        self.id = status
        conn.commit()
        conn.close()
        return True

    def getID(self):
        return self.id

# This is where the all the items will sit but the shop class is where the customer will be able to view the items and add them to the cart
class Item:
    def __init__(self):
        self.id = None
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

    def save_to_database(self, user: User):
        conn = sqlite3.connect('shop.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS items
                    (item_id INTEGER PRIMARY KEY, user_id INTEGER not null, name varchar(255) not null, amount INTEGER not null, price REAL not null)''')
        c.execute("INSERT OR REPLACE INTO items (user_id, name, amount, price) VALUES (?, ?, ?, ?)",
                  (user.getID(), self.name, self.amount, self.price))
        results = c.fetchall()

        print('Item.save_to_database', results)

        conn.commit()
        conn.close()
    
    def load_items_from_database(self, user: User):
        conn = sqlite3.connect('shop.db')
        c = conn.cursor()
        c.execute("SELECT item_id, name, amount, price FROM items")
        results = c.fetchall()

        self.items = [{'id': row[0], 'name': row[1], 'amount': row[2], 'price': row[3]} for row in results]
        
        conn.commit()
        conn.close()

    def view_items(self, user: User):
        self.load_items_from_database(user)
        if not self.items:
            print("\nSorry the shop is currently empty! Please Try again later.")
            return
        
        for item in self.items:
            print(f"(x{item['amount']}) {item['name']} ------- ${item['price']:.2f}")
    
    def delete_item(self, user: User, item_id):
        conn = sqlite3.connect('shop.db')
        c = conn.cursor()
        c.execute("DELETE FROM items WHERE item_id = ? AND user_id = ?", (item_id, user.getID()))
        conn.commit()
        conn.close()
        print(f"'{item_id}' has been deleted from our inventory.")

class Cart:
    def __init__(self):
        self.productID = None
        self.CategoryID = None

    def addToCart(self, user: User, item_id: int, amount: int):
        conn = sqlite3.connect('shop.db')
        c = conn.cursor()

        c.execute('''
        CREATE TABLE IF NOT EXISTS
            `cart` (
                `cart_id` INTEGER PRIMARY KEY,
                `user_id` INTEGER not null,
                `checkout` tinyint not null
            )
        ''')

        c.execute('''
        CREATE TABLE IF NOT EXISTS
            `cart_item` (
                `cart_item_id` INTEGER PRIMARY KEY,
                `cart_id` INTEGER not null,
                `item_id` INTEGER not null,
                `amount` INTEGER not null
            )
        ''')

        c.execute("SELECT * FROM cart WHERE user_id = ? AND checkout = ?", (user.getID(), 0))
        results = c.fetchall()


        if len(results) <= 0:   # cart does not exist
            c.execute("INSERT INTO cart (user_id, checkout) VALUES (?, ?) RETURNING cart_id", (user.getID(), 0))
            results = c.fetchall()
            conn.commit()

        cart_id = results[0][0]
        
        c.execute("INSERT INTO cart_item (cart_id, item_id, amount) VALUES (?, ?, ?)", (cart_id, item_id, amount))
        conn.commit()

        conn.close()
        pass

    def goBack(self):
        pass

    def viewCart(self, user: User):
        conn = sqlite3.connect('shop.db')
        c = conn.cursor()

        c.execute('''
        CREATE TABLE IF NOT EXISTS
            `cart` (
                `cart_id` INTEGER PRIMARY KEY,
                `user_id` INTEGER not null,
                `checkout` tinyint not null
            )
        ''')

        c.execute('''
        CREATE TABLE IF NOT EXISTS
            `cart_item` (
                `cart_item_id` INTEGER PRIMARY KEY,
                `cart_id` INTEGER not null,
                `item_id` INTEGER not null,
                `amount` INTEGER not null
            )
        ''')

        c.execute("SELECT * FROM cart WHERE user_id = ? AND checkout = ?", (user.getID(), 0))
        results = c.fetchall()

        if len(results) <= 0:
            print("There are no items in your cart!")
            return True

        cart_id = results[0][0]

        c.execute("SELECT item_id, amount FROM cart_item WHERE cart_id = ?", (cart_id,))
        results = c.fetchall()

        if len(results) <= 0:
            print("There are no items in your cart!")
            return True
        

        for item in results:
            c.execute("SELECT item_id, name, price FROM items WHERE item_id = ?", (item[0], ))
            newResults = c.fetchall()
            item_id, name, price = newResults[0]
            print(f"{item_id}: (x{item[1]}) {name} ------- ${price:.2f}")
        
        return True

    def remove(self):
        pass

    def checkOut(self, user: User):
        conn = sqlite3.connect('shop.db')
        c = conn.cursor()

        c.execute('''
        CREATE TABLE IF NOT EXISTS
            `cart` (
                `cart_id` INTEGER PRIMARY KEY,
                `user_id` INTEGER not null,
                `checkout` tinyint not null
            )
        ''')

        c.execute('''
        CREATE TABLE IF NOT EXISTS
            `cart_item` (
                `cart_item_id` INTEGER PRIMARY KEY,
                `cart_id` INTEGER not null,
                `item_id` INTEGER not null,
                `amount` INTEGER not null
            )
        ''')

        c.execute("SELECT * FROM cart WHERE user_id = ? AND checkout = ?", (user.getID(), 0))
        results = c.fetchall()

        if len(results) <= 0:
            print("\nThere are no items in your cart!")
            return False

        cart_id = results[0][0]

        c.execute("SELECT item_id, amount FROM cart_item WHERE cart_id = ?", (cart_id,))
        results = c.fetchall()

        for item in results:
            c.execute("UPDATE items SET amount = amount - ? WHERE item_id = ?", (item[1], item[0]))
            conn.commit()

        c.execute("UPDATE cart SET checkout = 1 WHERE user_id = ?", (user.getID(),))
        conn.commit()
        
        conn.close()
        return True

    def quantity(self, user: User, item_id: int, quantity: int):
        conn = sqlite3.connect('shop.db')
        c = conn.cursor()

        c.execute('''
        CREATE TABLE IF NOT EXISTS
            `cart` (
                `cart_id` INTEGER PRIMARY KEY,
                `user_id` INTEGER not null,
                `checkout` tinyint not null
            )
        ''')

        c.execute('''
        CREATE TABLE IF NOT EXISTS
            `cart_item` (
                `cart_item_id` INTEGER PRIMARY KEY,
                `cart_id` INTEGER not null,
                `item_id` INTEGER not null,
                `amount` INTEGER not null
            )
        ''')

        c.execute("SELECT * FROM cart WHERE user_id = ? AND checkout = ?", (user.getID(), 0))
        results = c.fetchall()

        if len(results) <= 0:
            print("\nThere are no items in your cart!")
            return True

        cart_id = results[0][0]

        if quantity <= 0:
            c.execute("DELETE FROM cart_item WHERE item_id = ? AND cart_id = ?", (item_id, cart_id))
            conn.commit()
            conn.close()

        else:
            c.execute("UPDATE cart_item SET amount = ? WHERE item_id = ? AND cart_id = ?", (quantity, item_id, cart_id))
            conn.commit()
            conn.close()

        return True




class Shop:
    def __init__(self):
        conn = sqlite3.connect('shop.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS items
                    (item_id INTEGER PRIMARY KEY, user_id INTEGER not null, name varchar(255) not null, amount INTEGER not null, price REAL not null)''')
        conn.commit()
        conn.close()

    def load_database(self):
        conn = sqlite3.connect('shop.db')
        c = conn.cursor()
        c.execute("SELECT item_id, name, price, amount FROM items")
        results = c.fetchall()
        conn.close()

        if not results:
            print("Sorry the shop is empty! Please try again later!")  
            return True 

        print("Items in the shop:")
        for row in results:
            id, name, price, amount = row
            print(f"{id}: (x{amount}) {name} ------- ${price:.2f}")
        return False 

