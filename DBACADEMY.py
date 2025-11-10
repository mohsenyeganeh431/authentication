import mysql.connector

class DataBase:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.crs = None

    def connect(self):
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database  
        )
        self.crs = self.conn.cursor()
        return self.conn, self.crs
    
    def setup(self):
        return self.connect()

    def close(self):
        
            self.conn.commit()
            self.crs.close()
            self.conn.close()