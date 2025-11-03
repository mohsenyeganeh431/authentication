from authentication import AuthSystem

def main():
    auth = AuthSystem()

    while True:
        print("\n=== Authentication System ===")
        print("1) Signup")
        print("2) Login")
        print("3) Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            auth.sign_up()

        elif choice == "2":
            auth.login()  

        elif choice == "3":
            print(" Goodbye! See you next time.")
            auth.close()
            break

        else:
            print(" Invalid choice, please try again.")



main()
