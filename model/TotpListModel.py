import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.DatabaseControl import DatabaseControl
from model.CryptControl import CryptControl


class TotpListModel:
    def __init__(self):
        self.__db_instance = DatabaseControl()
        self.__crypt = CryptControl()
    def encrypt_uri(self,username,passwd,uri,mailOrUser,plataform):
        try:    
            
            user_arrow = self.__db_instance.query_find_user_row_by_username(username=username)
            salt_crypt_base64_str = user_arrow[0][2]
            

            salt_crypt = self.__crypt.base64_decode(salt_crypt_base64_str)
            key = self.__crypt.derive_key_from_passwd(passwd=passwd,salt=salt_crypt)
            
            crypt_text_uri, iv = self.__crypt.encrypt(textPlain=uri,key=key)

            
            uri_crypt_base64 = self.__crypt.base64_encode(data_bytes=crypt_text_uri)
            iv__base64 = self.__crypt.base64_encode(data_bytes=iv)
           
            self.__db_instance.insert_totp(totpUriCrypt=uri_crypt_base64,iv=iv__base64,username=username,emailOrUser=mailOrUser,plataform=plataform)
            
        except:
            print("error no encrypt do uri ")
    def _decrypt_all_uri(self,username,password):
        #key
        user_arrow = self.__db_instance.query_find_user_row_by_username(username=username)
        salt_crypt_base64_str = user_arrow[0][2]
        #print(salt_crypt_base64_str)

        salt_crypt = self.__crypt.base64_decode(salt_crypt_base64_str)
        key = self.__crypt.derive_key_from_passwd(passwd=password,salt=salt_crypt)
        
        #totp stuff
        totp_rows = self.__db_instance.query_all_totp_rows_by_username(username=username)
        totp_list = list()
        for i in totp_rows:
            
            kid = i[0]
            uri_crypt_base64_str = i[2]
            iv_base64_str = i[3]
            emailOrUser = i[4]
            plataform = i[5]
            uri_crypt_data = self.__crypt.base64_decode(str_base64=uri_crypt_base64_str)
            iv_data = self.__crypt.base64_decode(str_base64=iv_base64_str)
            decrypt_uri_str = self.__crypt.decrypt(textEncrypt=uri_crypt_data,key=key,iv=iv_data)
            totp_list.append({"kid":kid,"uri":decrypt_uri_str,"emailOrUser":emailOrUser,"plataform":plataform})
        return totp_list
    
    def pre_settings_totpListView(self,username,password):
        is_empty_status = self._totp_db_is_empty(username=username)
        
        if is_empty_status != 1:
            return self._decrypt_all_uri(username=username,password=password)
        
    def _totp_db_is_empty(self,username):
        rows = self.__db_instance.query_all_totp_rows_by_username(username=username)
        if rows == []:
            return 1 
        return 0
    
    def totp_remove(self,kid):
        self.__db_instance.delete_totp_row(kid=kid)
    
    def totp_last_KID(self):
        row = self.__db_instance.query_last_totp_row()
        return row[0][0]
        

