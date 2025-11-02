from academyDB import DataBase

# connect to database
db = DataBase("localhost", "root", "zaq1XSW@", "academyDB")
db.create_database() 
conn, crs = db.connect()
db.create_tables()    


class AuthSystem:
    def __init__(self):
        self.db = db
        self.con, self.crs = self.db.connect()

    def sign_up(self):
        print("-------- SignUp -------")
        firstname = input("First name: ")
        lastname = input("Last name: ")
        username = input("Username: ")
        password = input("Password: ")
        repeat_password = input("Repeat Password: ")

        if password != repeat_password:
            print(" Passwords do not match!")
            return

        self.crs.execute("SELECT * FROM users WHERE username = %s", (username,))
        if self.crs.fetchone():
            print("This username already exists.")
            return

        self.crs.execute("""
            INSERT INTO users (firstname, lastname, username, password)
            VALUES (%s, %s, %s, %s)
        """, (firstname, lastname, username, password))
        self.con.commit()
        print(" Signup successful.")

    def login(self):
        print("-------- Login --------")
        username = input("Username: ")
        password = input("Password: ")

        self.crs.execute(
            "SELECT * FROM users WHERE username = %s AND password = %s",
            (username, password)
        )
        user = self.crs.fetchone()

        if user:
            print(f" Welcome, {user[1]} {user[2]}!")
        else:
            print("Username or password is incorrect.")

    def close(self):
        self.db.close()
