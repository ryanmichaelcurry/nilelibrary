class User:
    def __init__(self):
        self.id = None
        self.username = None
        self.status = None

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

    def getUsername(self):
        pass

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
        self.item_name = None
        self.amount = None
        self.price = None

    def setName(self, name):
        pass

    def setAmount(self, quantity):
        pass

    def subtractAmount(self, amount):
        pass

    def setPrice(self, price):
        pass

    def getName(self):
        pass

    def getAmount(self):
        pass

    def getPrice(self):
        pass


class Shop:
    def __init__(self):
