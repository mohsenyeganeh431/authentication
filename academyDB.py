import mysql.connector



class DataBase:
    
    def __init__ (self,host,user,password,database):
        
            
            self.host = host
            self.user = user
            self.password=password
            self.database = database
            self.con = None
            self.crs = None
            
        
    # Connect to MySQL
       
    def connect(self):
        
        self.con = mysql.connector.connect(
            
            host = self.host,
            user= self.user,
            password=self.password
        )
        self.crs  = self.con.cursor()
        
        return self.con , self.crs
        
    #create database
        
    def create_database(self):
        
        self.crs.execute("create database if not exists academyDB")
        self.con.database = "academyDB"
     
     
    #create tables
       
    def create_tabels(self):
        
        #profesor_tabel
        
        self.crs.execute("""
                         create table if not exists prof(
                             ID int primary key auto_increment,
                             name varchar(255) not null
                         )
                         """)
        
        #courses table
        
        self.crs.execute("""
        create table if not exists courses(
            ID int primary key auto_increment,
            name varchar(255) not null,
            time VARCHAR(50),
            code VARCHAR(50),
            professor_id INT,
            FOREIGN KEY (professor_id) REFERENCES prof(id)
                ON DELETE SET NULL
                ON UPDATE CASCADE
         )
         """)
        
        # Student table
        self.crs.execute("""
        CREATE TABLE IF NOT EXISTS student (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(100) NOT NULL
        )
        """)

        # Many-to-many tables
        self.crs.execute("""
        CREATE TABLE IF NOT EXISTS prof_course (
            prof_id INT,
            course_id INT,
            PRIMARY KEY (prof_id, course_id),
            FOREIGN KEY (prof_id) REFERENCES prof(id)
                ON DELETE CASCADE
                ON UPDATE CASCADE,
            FOREIGN KEY (course_id) REFERENCES courses(id)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        )
        """)
        
        self.crs.execute("""
        CREATE TABLE IF NOT EXISTS student_course (
            student_id INT,
            course_id INT,
            PRIMARY KEY (student_id, course_id),
            FOREIGN KEY (student_id) REFERENCES student(id)
                ON DELETE CASCADE
                ON UPDATE CASCADE,
            FOREIGN KEY (course_id) REFERENCES courses(id)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        )
        """)
        
        #users table
        
        self.crs.execute("""
                         
                         create table if not exists users(
                             
                             ID int primary key auto_increment,
                             
                             firstname varchar(100),
                             
                             lastname varchar(100),
                             
                             username varchar(100) unique not null,
                             
                             password varchar(100) not null                             
                             
                         )
                         
                         """)
        
    
        
        
    
    def close(self):
        
        self.con.commit()
        self.crs.close()
        self.con.close()
        
        
        
    
        
