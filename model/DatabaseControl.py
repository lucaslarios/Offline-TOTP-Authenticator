import os
import sqlite3





class DatabaseControl:
    __instance = None
    def __new__(cls):
       if DatabaseControl.__instance is None:
          DatabaseControl.__instance = super().__new__(cls)
       return DatabaseControl.__instance    
    
    def __init__(self):
        
        database_path = self._find_path(["database","database.db"])
        database_status = self._database_existence_verify(database_path)
        connection,cursor = self._database_connect(database_path)
        self._verify_database_creation(status=database_status,cursor=cursor,connection=connection)
        self.connection = connection
        self.cursor = cursor
    def _database_existence_verify(self,database_path):
        if not os.path.exists(database_path):
            return 0   
        else:
            return 1
        
       
    def _find_path(self,list): 
       path = os.getcwd()
       for  i in list: 
            path = os.path.join(path, i)
       return path 
    
    def _verify_database_creation(self,status,cursor,connection):
        if status == 0:
            self._create_database(cursor,connection)

    def _database_connect(self,database_path):
        try:
            connection = sqlite3.connect(database_path)
            cursor = connection.cursor()
            return connection,cursor
        except sqlite3.OperationalError as e:
            print("Erro na conexão com o Banco de Dados")
            print(e)
            
    
    def _create_database(self,cursor,connection):
        try:
            sql_statement = '''
                CREATE TABLE IF NOT EXISTS users 
                (
                        UID      INTEGER NOT NULL UNIQUE, 
                        username TEXT NOT NULL UNIQUE,
                        SALT_CRYPT TEXT NOT NULL,
                        SALT_PASSWD TEXT NOT NULL,
                        HASH_PASSWD TEXT NOT NULL,
                        blocked_date TEXT,      
                        PRIMARY KEY(UID AUTOINCREMENT) 
                );
                CREATE TABLE IF NOT EXISTS TOTP
                (
                        KID INTEGER NOT NULL UNIQUE,
                        UID INTEGER NOT NULL,
                        TOTP_URI_CRYPT TEXT NOT NULL,
                        IV TEXT NOT NULL,
                        emailOrUser TEXT NOT NULL,
                        plataform TEXT NOT NULL,
                        FOREIGN KEY("UID") REFERENCES users (UID),
                        PRIMARY KEY (KID AUTOINCREMENT)
                );
                
                '''
            cursor.executescript(sql_statement)
            connection.commit()
        except sqlite3.OperationalError as e:
            print("Erro na criação das tabelas do banco de dados")
            print(e)
            

    def insert_user(self,username,salt_crypt,salt_passwd,hash_passwd,blocked_time):#ok
        try:
            sql_statement = '''
                INSERT INTO users 
                (username,SALT_CRYPT,SALT_PASSWD,HASH_PASSWD,blocked_date)
                VALUES (?,?,?,?,?)
            '''
            data_tuple = (username,salt_crypt,salt_passwd,hash_passwd,blocked_time)
            self.cursor.execute(sql_statement,data_tuple)
            self.connection.commit()
            return 1
        except sqlite3.Error as error:
            print("Failed to insert da user into users table")
            return 0
    def insert_totp(self,totpUriCrypt,iv,username,emailOrUser,plataform):
        try:
            sql_statement = '''
                INSERT INTO TOTP 
                (UID,TOTP_URI_CRYPT,IV,emailOrUser,plataform)
                VALUES (?,?,?,?,?)
            '''
            
            uid = self._query_find_UID_by_username(username=username)
            data_tuple = (uid,totpUriCrypt,iv,emailOrUser,plataform)
            self.cursor.execute(sql_statement,data_tuple)
            self.connection.commit()
        except sqlite3.Error as error:
            print("Failed to insert da user into TOTP table")
    
    def query_find_user_row_by_username(self,username):
        try:
            self.cursor.execute("SELECT * FROM users WHERE username =?",(username,))
            row = self.cursor.fetchall()
            return row
        except sqlite3.OperationalError as e:
            print(e)
            return 

    def _query_find_UID_by_username(self,username):
        username_info = self.query_find_user_row_by_username(username=username)
        uid = username_info[0][0]
        return uid

    def query_all_totp_rows_by_username(self,username):
        uid = self._query_find_UID_by_username(username=username)
        try: 
            self.cursor.execute("select * from TOTP WHERE UID =?",(uid,))
            rows = self.cursor.fetchall()
            return rows
        except sqlite3.OperationalError as e:
            print(e)
    
    def delete_totp_row(self,kid):
                
        sql = 'DELETE FROM TOTP WHERE kid = ?'

        try:
            self.cursor.execute(sql,(kid,))
            self.connection.commit()
        except sqlite3.OperationalError as e:
            print(e)
    
    def query_last_totp_row(self):
        sql = "SELECT * FROM TOTP ORDER BY KID DESC LIMIT 1"
        try:
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            return rows
        except sqlite3.OperationalError as e:
            print(e)

    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("The SQLite connection is closed")

    

