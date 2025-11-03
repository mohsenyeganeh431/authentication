from DBACADEMY import DataBase

# connect to database 
db = DataBase("localhost", "root", "zaq1XSW@", "academyDB")
db.setup()
conn, crs = db.connect()


class AuthSystem:
    def __init__(self):
        self.con = conn
        self.crs = crs

    # ---------------- SignUp ----------------
    def sign_up(self):
        print("\n-------- Sign Up --------")
        fn = input("First name: ").strip()
        ln = input("Last name: ").strip()
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        repeat = input("Repeat Password: ").strip()

        if password != repeat:
            print("Passwords do not match!")
            return

        self.crs.execute("SELECT id FROM users WHERE username=%s", (username,))
        if self.crs.fetchone():
            print("Username already exists.")
            return



        
        self.crs.execute("SELECT id FROM roles WHERE role_name='user'")
        role_id = self.crs.fetchone()[0]

        self.crs.execute("""
            INSERT INTO users (firstname, lastname, username, password, role_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (fn, ln, username, password, role_id))
        self.con.commit()
        print("Signup successful!")



    # ---------------- Login ----------------
    def login(self):
        print("\n-------- Login --------")
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        self.crs.execute("""
            SELECT u.id, u.firstname, u.lastname, r.role_name
            FROM users u
            LEFT JOIN roles r ON u.role_id = r.id
            WHERE u.username=%s AND u.password=%s
        """, (username, password))
        user = self.crs.fetchone()

        if not user:
            print("Invalid username or password.")
            return

        uid, fn, ln, role = user
        print(f"Welcome {fn} {ln}! (role: {role})")

        if role == "owner":
            self.owner_menu(uid)
        elif role == "admin":
            self.admin_menu(uid)
        else:
            self.user_menu(uid)

    # ---------------- Owner Menu ----------------
    def owner_menu(self, uid):
        while True:
            print("\n=== Owner Menu ===")
            print("1) View all users")
            print("2) Create new user")
            print("3) Delete user")
            print("4) Logout")

            choice = input("Choice: ").strip()
            if choice == "1":
                self.view_users()
            elif choice == "2":
                self.create_user()
            elif choice == "3":
                self.delete_user(uid, allow_all=True)
            elif choice == "4":
                break
            else:
                print(" Invalid choice.")

    # ---------------- Admin Menu ----------------
    def admin_menu(self, uid):
        while True:
            print("\n=== Admin Menu ===")
            print("1) View all users")
            print("2) Create user (only 'user')")
            print("3) Delete user (only 'user')")
            print("4) Logout")

            choice = input("Choice: ").strip()
            if choice == "1":
                self.view_users()
            elif choice == "2":
                self.create_user(role_limit="user")
            elif choice == "3":
                self.delete_user(uid, allow_all=False)
            elif choice == "4":
                break
            else:
                print(" Invalid choice.")

    # ---------------- User Menu ----------------
    def user_menu(self, uid):
        while True:
            print("\n=== User Menu ===")
            print("1) View my profile")
            print("2) Edit my name")
            print("3) Change my password")
            print("4) Logout")

            choice = input("Choice: ").strip()
            if choice == "1":
                self.view_profile(uid)
            elif choice == "2":
                self.edit_name(uid)
            elif choice == "3":
                self.change_password(uid)
            elif choice == "4":
                break
            else:
                print("Invalid choice.")

    # ---------------- Shared Operations ----------------
    def view_users(self):
        self.crs.execute("""
            SELECT u.id, u.username, u.firstname, u.lastname, r.role_name
            FROM users u
            LEFT JOIN roles r ON u.role_id = r.id
            ORDER BY u.id
        """)
        rows = self.crs.fetchall()

        print(f"\n{'ID':<4} {'Username':<15} {'Name':<25} {'Role':<10}")
        for i, u, f, l, r in rows:
            print(f"{i:<4} {u:<15} {f+' '+l:<25} {r:<10}")

    def create_user(self, role_limit=None):
        fn = input("First name: ").strip()
        ln = input("Last name: ").strip()
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        if role_limit:
            role_name = role_limit
        else:
            self.crs.execute("SELECT role_name FROM roles")
            roles = [r[0] for r in self.crs.fetchall()]
            print(f"Available roles: {', '.join(roles)}")
            role_name = input("Role: ").strip()
            if role_name not in roles:
                print("Invalid role, defaulting to 'user'.")
                role_name = "user"

        self.crs.execute("SELECT id FROM roles WHERE role_name=%s", (role_name,))
        role_id = self.crs.fetchone()[0]

        self.crs.execute("""
            INSERT INTO users (firstname, lastname, username, password, role_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (fn, ln, username, password, role_id))
        self.con.commit()
        print("User created successfully.")

    def delete_user(self, current_id, allow_all=False):
        self.view_users()
        try:
            uid = int(input("Enter user ID to delete: ").strip())
        except ValueError:
            print("Invalid ID.")
            return

        if uid == current_id:
            print("You can't delete yourself.")
            return

        if not allow_all:
            self.crs.execute("""
                SELECT r.role_name FROM users u
                JOIN roles r ON u.role_id=r.id
                WHERE u.id=%s
            """, (uid,))
            row = self.crs.fetchone()
            if not row or row[0] != "user":
                print("Admins can only delete normal users.")
                return

        self.crs.execute("DELETE FROM users WHERE id=%s", (uid,))
        self.con.commit()
        print("User deleted successfully.")

    # ---------------- User Functions ----------------
    def view_profile(self, uid):
        self.crs.execute("""
            SELECT u.firstname, u.lastname, u.username, r.role_name
            FROM users u
            LEFT JOIN roles r ON u.role_id=r.id
            WHERE u.id=%s
        """, (uid,))
        user = self.crs.fetchone()
        print("\n--- My Profile ---")
        print(f"Name: {user[0]} {user[1]}")
        print(f"Username: {user[2]}")
        print(f"Role: {user[3]}")

    def edit_name(self, uid):
        fn = input("New first name: ").strip()
        ln = input("New last name: ").strip()
        self.crs.execute("UPDATE users SET firstname=%s, lastname=%s WHERE id=%s", (fn, ln, uid))
        self.con.commit()
        print("Name updated successfully.")

    def change_password(self, uid):
        old = input("Current password: ").strip()
        self.crs.execute("SELECT password FROM users WHERE id=%s", (uid,))
        real_pass = self.crs.fetchone()[0]

        if old != real_pass:
            print("Incorrect current password.")
            return

        new = input("New password: ").strip()
        repeat = input("Repeat new password: ").strip()
        if new != repeat:
            print("Passwords do not match.")
            return

        self.crs.execute("UPDATE users SET password=%s WHERE id=%s", (new, uid))
        self.con.commit()
        print("Password updated successfully.")

    def close(self):
        self.con.commit()
        self.crs.close()
        self.con.close()
