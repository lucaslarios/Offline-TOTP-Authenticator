
from model.DatabaseControl import DatabaseControl
from model.CryptControl import CryptControl

class LoginModel:
    def __init__(self):
        self.__databaseControl = DatabaseControl()
        self.__cryptControl = CryptControl()
    def login_user(self,username,password):
        user_response = self.__detect_and_get_user_in_database(username=username)
        user_existence_status = user_response[0] 
        user_row = user_response[1]
        if user_existence_status != 1:
            return 0 
        passwd_auth_status = self.__passwd_auth(user_row=user_row,passwd=password)
        if passwd_auth_status !=1:
            return 0 
        return 1

    def __detect_and_get_user_in_database(self,username):
        query = self.__databaseControl.query_find_user_row_by_username(username=username)        
        if query != []:
            return [1,query] #[status,query]
        else:
            return [0,None] 

    def __passwd_auth(self,user_row,passwd):
        salt_passwd_base64_str = user_row[0][3]
        hash_passwd_base64_str = user_row[0][4]
        salt_passwd = self.__cryptControl.base64_decode(str_base64=salt_passwd_base64_str)
        hash_passwd = self.__cryptControl.base64_decode(str_base64=hash_passwd_base64_str)
        passwd_auth_status = self.__cryptControl.passwd_storage_verify(salt=salt_passwd,passwd=passwd,password_storaged=hash_passwd)
        return passwd_auth_status




