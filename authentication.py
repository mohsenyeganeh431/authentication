# Import DataBase class from DBACADEMY module
from DBACADEMY import DataBase

# Connect to database with specified credentials
db = DataBase("localhost", "root", "zaq1XSW@", "academyDB")
db.setup()  # Initialize database (create tables and default data)
conn, crs = db.connect()  # Get connection and cursor

class AuthSystem:
    def __init__(self):
        # Store connection and cursor in class variables
        self.con = conn
        self.crs = crs

    # ---------------- SignUp ----------------
    def sign_up(self):
        print("\n-------- Sign Up --------")
        # Get user information
        fn = input("First name: ").strip()  # First name
        ln = input("Last name: ").strip()   # Last name
        username = input("Username: ").strip()  # Username
        password = input("Password: ").strip()  # Password
        repeat = input("Repeat Password: ").strip()  # Password confirmation

        # Check if passwords match
        if password != repeat:
            print("Passwords do not match!")
            return  # Exit method if passwords don't match

        # Check if username already exists
        self.crs.execute("SELECT id FROM users WHERE username=%s", (username,))
        if self.crs.fetchone():  # If user with this username exists
            print("Username already exists.")
            return  # Exit method

        # Find the role ID for 'user' role
        self.crs.execute("SELECT id FROM roles WHERE role_name='user'")
        role_id = self.crs.fetchone()[0]  # Get the first column from result (ID)

        # Insert new user into database
        self.crs.execute("""
            INSERT INTO users (firstname, lastname, username, password, role_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (fn, ln, username, password, role_id))
        self.con.commit()  # Save changes to database
        print("Signup successful!")

    # ---------------- Login ----------------
    def login(self):
        print("\n-------- Login --------")
        # Get login credentials
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        # Search for user in database with username and password
        self.crs.execute("""
            SELECT u.id, u.firstname, u.lastname, r.role_name
            FROM users u
            LEFT JOIN roles r ON u.role_id = r.id
            WHERE u.username=%s AND u.password=%s
        """, (username, password))
        user = self.crs.fetchone()  # Get first result

        # If no user found
        if not user:
            print("Invalid username or password.")
            return

        # Extract user information from query result
        uid, fn, ln, role = user
        print(f"Welcome {fn} {ln}! (role: {role})")

        # Redirect user to appropriate menu based on their role
        if role == "owner":
            self.owner_menu(uid)
        elif role == "admin":
            self.admin_menu(uid)
        else:
            self.user_menu(uid)

    # ---------------- Owner Menu ----------------
    def owner_menu(self, uid):
        while True:  # Infinite loop until user logs out
            print("\n=== Owner Menu ===")
            print("1) View all users")    # View all users
            print("2) Create new user")   # Create new user
            print("3) Delete user")       # Delete user
            print("4) Logout")           # Logout

            choice = input("Choice: ").strip()
            if choice == "1":
                self.view_users()  # Display all users
            elif choice == "2":
                self.create_user()  # Create new user (any role)
            elif choice == "3":
                self.delete_user(uid, allow_all=True)  # Delete any user
            elif choice == "4":
                break  # Exit loop and return to main menu
            else:
                print(" Invalid choice.")  # Invalid choice

    # ---------------- Admin Menu ----------------
    def admin_menu(self, uid):
        while True:
            print("\n=== Admin Menu ===")
            print("1) View all users")     # View all users
            print("2) Create user (only 'user')")  # Only create regular users
            print("3) Delete user (only 'user')")  # Only delete regular users
            print("4) Logout")

            choice = input("Choice: ").strip()
            if choice == "1":
                self.view_users()
            elif choice == "2":
                self.create_user(role_limit="user")  # Role limited to "user"
            elif choice == "3":
                self.delete_user(uid, allow_all=False)  # Only regular users
            elif choice == "4":
                break
            else:
                print(" Invalid choice.")

    # ---------------- User Menu ----------------
    def user_menu(self, uid):
        while True:
            print("\n=== User Menu ===")
            print("1) View my profile")    # View own profile
            print("2) Edit my name")       # Edit name
            print("3) Change my password") # Change password
            print("4) Logout")            # Logout

            choice = input("Choice: ").strip()
            if choice == "1":
                self.view_profile(uid)    # Display current user's profile
            elif choice == "2":
                self.edit_name(uid)       # Edit current user's name
            elif choice == "3":
                self.change_password(uid) # Change current user's password
            elif choice == "4":
                break
            else:
                print("Invalid choice.")

    # ---------------- Shared Operations ----------------
    def view_users(self):
        # Get all users with their roles
        self.crs.execute("""
            SELECT u.id, u.username, u.firstname, u.lastname, r.role_name
            FROM users u
            LEFT JOIN roles r ON u.role_id = r.id
            ORDER BY u.id
        """)
        rows = self.crs.fetchall()  # Get all results

        # Print table header
        print(f"\n{'ID':<4} {'Username':<15} {'Name':<25} {'Role':<10}")
        
        # Print each user in a row
        for i, u, f, l, r in rows:
            print(f"{i:<4} {u:<15} {f+' '+l:<25} {r:<10}")

    def create_user(self, role_limit=None):
        # Get new user information
        fn = input("First name: ").strip()
        ln = input("Last name: ").strip()
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        # Determine user role
        if role_limit:  # If role is limited (e.g., for admin)
            role_name = role_limit
        else:  # If role is not limited (for owner)
            # Get all available roles
            self.crs.execute("SELECT role_name FROM roles")
            roles = [r[0] for r in self.crs.fetchall()]
            print(f"Available roles: {', '.join(roles)}")
            role_name = input("Role: ").strip()
            
            # If role is invalid, default to "user"
            if role_name not in roles:
                print("Invalid role, defaulting to 'user'.")
                role_name = "user"

        # Find the ID of selected role
        self.crs.execute("SELECT id FROM roles WHERE role_name=%s", (role_name,))
        role_id = self.crs.fetchone()[0]

        # Insert new user into database
        self.crs.execute("""
            INSERT INTO users (firstname, lastname, username, password, role_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (fn, ln, username, password, role_id))
        self.con.commit()
        print("User created successfully.")

    def delete_user(self, current_id, allow_all=False):
        self.view_users()  # Display user list
        try:
            uid = int(input("Enter user ID to delete: ").strip())  # Get user ID to delete
        except ValueError:  # If user didn't enter a number
            print("Invalid ID.")
            return

        # Prevent user from deleting themselves
        if uid == current_id:
            print("You can't delete yourself.")
            return

        # If user is admin and can only delete regular users
        if not allow_all:
            # Check role of user to be deleted
            self.crs.execute("""
                SELECT r.role_name FROM users u
                JOIN roles r ON u.role_id=r.id
                WHERE u.id=%s
            """, (uid,))
            row = self.crs.fetchone()
            
            # If user is admin or owner, don't allow deletion
            if not row or row[0] != "user":
                print("Admins can only delete normal users.")
                return

        # Delete user from database
        self.crs.execute("DELETE FROM users WHERE id=%s", (uid,))
        self.con.commit()
        print("User deleted successfully.")

    # ---------------- User Functions ----------------
    def view_profile(self, uid):
        # Get current user's profile information
        self.crs.execute("""
            SELECT u.firstname, u.lastname, u.username, r.role_name
            FROM users u
            LEFT JOIN roles r ON u.role_id=r.id
            WHERE u.id=%s
        """, (uid,))
        user = self.crs.fetchone()
        
        # Display information
        print("\n--- My Profile ---")
        print(f"Name: {user[0]} {user[1]}")
        print(f"Username: {user[2]}")
        print(f"Role: {user[3]}")

    def edit_name(self, uid):
        # Get new name
        fn = input("New first name: ").strip()
        ln = input("New last name: ").strip()
        
        # Update name in database
        self.crs.execute("UPDATE users SET firstname=%s, lastname=%s WHERE id=%s", (fn, ln, uid))
        self.con.commit()
        print("Name updated successfully.")

    def change_password(self, uid):
        # Get current password
        old = input("Current password: ").strip()
        
        # Verify current password is correct
        self.crs.execute("SELECT password FROM users WHERE id=%s", (uid,))
        real_pass = self.crs.fetchone()[0]

        if old != real_pass:
            print("Incorrect current password.")
            return

        # Get new password
        new = input("New password: ").strip()
        repeat = input("Repeat new password: ").strip()
        
        # Check if new passwords match
        if new != repeat:
            print("Passwords do not match.")
            return

        # Update password
        self.crs.execute("UPDATE users SET password=%s WHERE id=%s", (new, uid))
        self.con.commit()
        print("Password updated successfully.")

    def close(self):
        self.con.commit()  # Final save of changes
        self.crs.close()   # Close cursor
        self.con.close()   # Close connection