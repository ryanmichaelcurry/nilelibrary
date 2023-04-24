from classes import User, Cart, Shop, Item

# Main menu function
def main_menu():
    while True:
        print("Hello welcom to Nile Library!")
        print("--- Login ---")
        username = input("Enter your username: ")
        password = user.getPass("Enter your password: ") #I kind of am winging it here, not really sure how to do the log in stuff
        user = User()
        if user.login(username, password):
            print("Login successful!")
            break
        else:
            print("Invalid username or password. Please try again.")

    while True:
        # I just used this as a place holder we can change 1 and 2 to whatever we want to. I assume that if 
        # we are having stutus for people changing the inventory we should have a seperate menu for them that adds
        # the inventory tab.
        if user.getStatus == "1": 
            print("\n--- Main Menu ---")
            print("1. User")
            print("2. Cart")
            print("3. Shop")
            print("4. Exit")
            choice = input("Please enter a number: ")

            if choice == "1":
                user_menu()
            elif choice == "2":
                cart_menu()
            elif choice == "3":
                shop_menu()
            elif choice == "4":
                print("Have a nice day!")
                break
            else:
                print("Invalid choice! Please try again.")

        if user.getStatus == "2":
            print("\n--- Main Menu ---")
            print("1. User")
            print("2. Cart")
            print("3. Inventory")
            print("4. Shop")
            print("5. Exit")
            choice = input("Please enter a number: ")

            if choice == "1":
                user_menu()
            elif choice == "2":
                cart_menu()
            elif choice == "3":
                item_menu()
            elif choice == "4":
                shop_menu()
            elif choice == "5":
                print("Have a nice day!")
                break
            else:
                print("Invalid choice! Please try again.")

# User
def user_menu():
    user = User()

    user.login()
    user.signup()
    user.signout()
    user.getStatus()
    user.setStatus()
    user.getUsername()
    user.getID()

# Cart
def cart_menu():
    cart = Cart() 

    cart.goBack()
    cart.viewCart()
    cart.remove()
    cart.shipping()
    cart.quantity()

# Item / inventory
def item_menu():
    item = Item()
    
    while True: 
        print("\n--- Inventory ---")
        print("1. Add an Inventory")
        print("2. View Inventory")
        print("3. Return to Main Menu")
        choice = input("Enter a number: ")

        if choice == "1":
            name = input("\nEnter item name: ")
            item.setName(name)

            amount = int(input("Enter item amount: "))
            item.setAmount(amount)

            price = float(input("Enter item price: $"))
            item.setPrice(price)

            item.save_to_database()

            print("Item saved to database.\n")

        elif choice == "2":
            print("\n")
            item.view_items()

        elif choice == "3":
            break

def shop_menu():
    while True:
        print("\n----- Shop -----")
        shop = Shop()
        shop.view_items()

        choice = input("\nTo return to the Main Menu please input 1: ")
        if choice == "1":
            break
        else:
            print("Ok stay for a while! Continue browsing!")

    
if __name__ == "__main__":
    main_menu()