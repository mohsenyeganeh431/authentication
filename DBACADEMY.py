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
        temp_con = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password
        )
        temp_crs = temp_con.cursor()
        temp_crs.execute("CREATE DATABASE IF NOT EXISTS academyDB")
        temp_con.close()

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

        self.crs.execute("""
            CREATE TABLE IF NOT EXISTS users(
                ID INT PRIMARY KEY AUTO_INCREMENT,
                firstname VARCHAR(100),
                lastname VARCHAR(100),
                username VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(100) NOT NULL,
                role_id int,
                foreign key (role_id) references roles(id)
                            on delete set null
                            on update cascade
            )
        """)
        
        self.crs.execute("""
                         
                         create table if not exist roles(
                             
                             id int primary key auto_increment,
                             role_name varchar(100) unique not null
             )

         """)

    def close(self):
        self.con.commit()
        self.crs.close()
        self.con.close()
