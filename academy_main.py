from authentication import AuthSystem

def main():
    auth1 = AuthSystem()

    while True:
        print("\n=== Authentication System ===")
        print("1) Signup")
        print("2) Login")
        print("3) Exit")

        choice = input("Enter your choice: ")

        match choice:
            case "1":
                auth1.sign_up()
            case "2":
                auth1.login()
            case "3":
                auth1.close()
                print("Goodbye ")
                break
            case _:
                print(" Invalid choice!")



main()
