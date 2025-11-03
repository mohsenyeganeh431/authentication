import mysql.connector

class DataBase:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.con = None
        self.crs = None

    # connect to  MySQL
    def connect(self):
        self.con = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database  
        )
        self.crs = self.con.cursor()
        return self.con, self.crs

    #create database if not exists
    def create_database(self):
        con = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password
        )
        crs = con.cursor()
        crs.execute("CREATE DATABASE IF NOT EXISTS academyDB")
        con.close()

    # create tables
    def create_tables(self):
        self.crs.execute("""
            CREATE TABLE IF NOT EXISTS prof(
                ID INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(255) NOT NULL
            )
        """)

        self.crs.execute("""
            CREATE TABLE IF NOT EXISTS courses(
                ID INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(255) NOT NULL,
                time VARCHAR(50),
                code VARCHAR(50),
                professor_id INT,
                FOREIGN KEY (professor_id) REFERENCES prof(ID)
                    ON DELETE SET NULL
                    ON UPDATE CASCADE
            )
        """)

        self.crs.execute("""
            CREATE TABLE IF NOT EXISTS student(
                ID INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(100) NOT NULL
            )
        """)

        self.crs.execute("""
            CREATE TABLE IF NOT EXISTS prof_course(
                prof_id INT,
                course_id INT,
                PRIMARY KEY (prof_id, course_id),
                FOREIGN KEY (prof_id) REFERENCES prof(ID)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE,
                FOREIGN KEY (course_id) REFERENCES courses(ID)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
            )
        """)

        self.crs.execute("""
            CREATE TABLE IF NOT EXISTS student_course(
                student_id INT,
                course_id INT,
                PRIMARY KEY (student_id, course_id),
                FOREIGN KEY (student_id) REFERENCES student(ID)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE,
                FOREIGN KEY (course_id) REFERENCES courses(ID)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
            )
        """)

        #role table
        self.crs.execute("""
            CREATE TABLE IF NOT EXISTS roles (
                id INT PRIMARY KEY AUTO_INCREMENT,
                role_name VARCHAR(50) UNIQUE NOT NULL
            )
        """)

        # user table
        self.crs.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT PRIMARY KEY AUTO_INCREMENT,
                firstname VARCHAR(100),
                lastname VARCHAR(100),
                username VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(100) NOT NULL,
                role_id INT,
                FOREIGN KEY (role_id) REFERENCES roles(id)
                    ON DELETE SET NULL
                    ON UPDATE CASCADE
            )
        """)
        
    def setup(self):
    
        self.create_database()
        self.connect()
        self.create_tables()
        

    def close(self):
        self.con.commit()
        self.crs.close()
        self.con.close()
