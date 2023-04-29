from classes import User, Cart, Shop, Item

# Main menu function
def main_menu():
    while True:
        print("Hello welcome to Nile Library!")
        print("--- Login ---")
        username = input("Enter your username: ")
        password = input("Enter your password: ") #I kind of am winging it here, not really sure how to do the log in stuff
        user = User(username, password)
        if user.signup():
            print("Registration successful!")
            user.login()
            break
        else:
            if user.login():
                print("Login successful!")
                break
            else:
                print("Invalid username or password. Please try again.")

    while True:
        # I just used this as a place holder we can change 1 and 2 to whatever we want to. I assume that if 
        # we are having stutus for people changing the inventory we should have a seperate menu for them that adds
        # the inventory tab.
        if user.getStatus() == 1: 
            print("\n--- Main Menu ---")
            print("1. User")
            print("2. Cart")
            print("3. Shop")
            print("4. Exit")
            choice = input("Please enter a number: ")

            if choice == "1":
                user_menu(user)
            elif choice == "2":
                cart_menu(user)
            elif choice == "3":
                shop_menu(user)
            elif choice == "4":
                print("Have a nice day!")
                break
            else:
                print("Invalid choice! Please try again.")

        if user.getStatus() == 2:
            print("\n--- Main Menu ---")
            print("1. User")
            print("2. Cart")
            print("3. Inventory")
            print("4. Shop")
            print("5. Exit")
            choice = input("Please enter a number: ")

            if choice == "1":
                user_menu(user)
            elif choice == "2":
                cart_menu(user)
            elif choice == "3":
                item_menu(user)
            elif choice == "4":
                shop_menu(user)
            elif choice == "5":
                print("Have a nice day!")
                break
            else:
                print("Invalid choice! Please try again.")

# User
def user_menu(user: User):
    cart = Cart()

    while True:
        print("\n--- User Menu ---")
        print("1. Order History")
        print("2. Edit Shipping Information")
        print("3. Edit Payment Information")
        print("4. Delete Account")
        print("5. Return to Main Menu")
        choice = input("Please enter a number: ")

        if choice == "1":
            print("\n")
            user.getOrderHistory()
        elif choice == "2":
            address = input("Please enter your full address: ")
            user.setAddress(address)
        elif choice == "3":
            credit_card = input("Please enter your Credit Card: ")
            user.setCreditCard(credit_card)
        elif choice == "4":
            confirmation = input("Are you sure (Y/N): ")
            if confirmation == "Y":
                if user.deleteAccount():
                    main_menu()
                    
        #Return to Main Menu
        elif choice == "5":
            break
        elif choice == "6":
            user.setStatus(2)
            break

# Cart
def cart_menu(user: User):
    cart = Cart()

    while True:
        print("\n--- Cart Menu ---")
        print("1. View Cart")
        print("2. Checkout Cart")
        print("3. Remove Item")
        print("4. Edit Item's Quantity")
        print("5. Return to Main Menu")
        choice = input("Please enter a number: ")

        if choice == "1":
            print("\n")
            cart.viewCart(user)
        elif choice == "2":
            cart.checkOut(user)
        elif choice == "3":
            item_id = int(input("Item ID: "))
            cart.quantity(user, item_id, 0)
        elif choice == "4":
            item_id = int(input("Item ID: "))
            quantity = int(input("Quantity: x"))
            cart.quantity(user, item_id, quantity)
        #Return to Main Menu
        elif choice == "5":
            break

# Item / inventory
def item_menu(user):
    item = Item()
    
    while True: 
        print("\n--- Inventory ---")
        print("1. Add an Inventory")
        print("2. View Inventory")
        print("3. Delete Item")
        print("4. Return to Main Menu")
        choice = input("Enter a number: ")

        #Add Item
        if choice == "1":
            name = input("\nEnter item name: ")
            item.setName(name)

            amount = int(input("Enter amount: "))
            item.setAmount(amount)

            price = float(input("Enter item price: $"))
            item.setPrice(price)

            item.save_to_database(user)

            print("Item saved to database.\n")

        #View Inventory
        elif choice == "2":
            print("\n")
            item.view_items(user)

        #Remove Items Completely
        elif choice == "3":
            item_id = input("Which Item would like to delete?: ")
            item.delete_item(user, item_id)

        #Return to Main Menu
        elif choice == "4":
            break

def shop_menu(user):
    shop = Shop()
    cart = Cart()

    while True:
        print("\n----- Shop -----")
        print("1. View Shop")
        print("2. Add to Cart")
        print("3. Return to Main Menu")
        choice = input("What would you like to do?: ")

        if choice == "1":
            print("\n")
            is_empty = shop.load_database()
            if is_empty:
                continue
        
        elif choice == "2":
            print("\n")
            is_empty = shop.load_database()
            if is_empty:
                continue
            else:
                print("\nPlease enter the ID of the item you would like to add as well as the quantity! ")
                item = input("Item ID: ")
                amount = input("Quantity: x")
                cart.addToCart(user, item, amount)

        elif choice == "3":
            break

        else:
            print("Sorry that was an invalid choice, please try again!")


    
if __name__ == "__main__":
    main_menu()