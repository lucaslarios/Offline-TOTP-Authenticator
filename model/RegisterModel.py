import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.DatabaseControl import DatabaseControl
from model.CryptControl import CryptControl
class RegisterModel:
    def __init__(self):                
        self.__db_instance = DatabaseControl()
        self.__crypt = CryptControl()
    def create_user(self,username,passwd):
        
        self.__salt_crypt = self.__crypt.generate_salt()
        self.__salt_crypt_base64 = self.__crypt.base64_encode(data_bytes=self.__salt_crypt)
        
        self.__salt_passwd = self.__crypt.generate_salt()
        self.__salt_passwd_base64 = self.__crypt.base64_encode(data_bytes=self.__salt_passwd) 

        self.__hash_passwd =self.__crypt.passwd_storage_creator(salt=self.__salt_passwd,passwd=passwd)
        self.__hash_passwd_base64 =  self.__crypt.base64_encode(data_bytes=self.__hash_passwd)
        status = self.__db_instance.insert_user(
            username=username,
            salt_crypt=self.__salt_crypt_base64,
            salt_passwd=self.__salt_passwd_base64,
            hash_passwd=self.__hash_passwd_base64,
            blocked_time="None",
            )
        return  status  
    
            
                
 
