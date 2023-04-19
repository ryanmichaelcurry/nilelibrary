from classes import User, Cart, Inventory

# Main menu function
def main_menu():
    while True:
        print("Hello welcom to Nile Library!")
        print("--- Login ---")
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        user = User()
        if user.login(username, password):
            print("Login successful!")
            break
        else:
            print("Invalid username or password. Please try again.")

    while True:
        print("\n--- Main Menu ---")
        print("1. User")
        print("2. Cart")
        print("3. Inventory")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            user_menu()
        elif choice == "2":
            cart_menu()
        elif choice == "3":
            inventory_menu()
        elif choice == "4":
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

# Inventory
def inventory_menu():
    inventory = Inventory() 

    inventory.setName()
    inventory.setAmount()
    inventory.subtractAmount()
    inventory.setPrice()
    inventory.getName()
    inventory.getAmount()
    inventory.getPrice()

if __name__ == "__main__":
    main_menu()