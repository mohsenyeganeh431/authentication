from academyDB import DataBase

db = DataBase("localhost", "root", "zaq1XSW@", "academyDB")
db.connect() 
db.create_database()

class AuthSystem:
    
    def __init__(self):
        self.db = db
        self.conn, self.crs = self.db.connect() 

    def sign_up(self):
        """Sign up new user"""
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
            print(" This username already exists.")
            return

        self.crs.execute("""
            INSERT INTO users (firstname, lastname, username, password)
            VALUES (%s, %s, %s, %s)
        """, (firstname, lastname, username, password))
        self.con.commit() 

        print("Signup successful.")

    def login(self):
        """Login user"""
        print("--- Login ---")
        username = input("Username: ")
        password = input("Password: ")

        self.crs.execute(
            "SELECT * FROM users WHERE username = %s AND password = %s",
            (username, password)
        )
        user = self.crs.fetchone()  

        if user:
            print(f" Welcome !")
        else:
            print(" Username or password is incorrect.")

    def close(self):
        self.db.close()
