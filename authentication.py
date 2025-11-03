from DBACADEMY import DataBase

# connect to database
db = DataBase("localhost", "root", "zaq1XSW@", "academyDB")
db.setup() 
conn, crs = db.connect()
  



class AuthSystem:
    def __init__(self):
        self.con = conn
        self.crs = crs 

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
        
        self.crs.execute("SELECT id FROM roles WHERE role_name='user'")
        role_id  = self.crs.fetchone()[0]

        self.crs.execute("""
            INSERT INTO users (firstname, lastname, username, password, role_id)
            VALUES (%s, %s, %s, %s,%s)
        """, (firstname, lastname, username, password, role_id))
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
