import tkinter as tk
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.RegisterModel import RegisterModel
from model.LoginModel import LoginModel
from model.Totp import Totp
from model.TotpListModel import TotpListModel
from view.loginView import LoginPage
from view.registerView import RegisterPage
from view.TotpPage import TotpPage

class Controller:
    def __init__(self):
        self.__registerModel = RegisterModel()
        self._loginModel = LoginModel()
        self._totpListModel = TotpListModel()
        self.username = ""
        self.password = ""
        self.app = tk.Tk()
        self.app.title("Authenticator")
        self.app.geometry("300x450")
        self.app.resizable(False, False)
        screen_width = self.app.winfo_screenwidth()
        screen_height = self.app.winfo_screenheight()
        position_x = (screen_width // 2) - (300 // 2)
        position_y = (screen_height // 2) - (400 // 2)
        self.app.geometry(f"300x400+{position_x}+{position_y}")
        container = tk.Frame(self.app, bg="#f4f4f4")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginPage, RegisterPage,TotpPage):
            page_name = F.__name__
            frame = F(container, self)  
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def run(self):
        self.show_frame("LoginPage") 
        self.app.mainloop()
    
    def register_user_controller(self,username,password):
        return self.__registerModel.create_user(username=username,passwd=password)
        
    def login_user_auth_controller(self,username,password):
        return self._loginModel.login_user(username=username,password=password)
    def totp_number_controller(self,uri):
        return Totp().totp_number(uri=uri)
    def totp_time_controller(self):
        return Totp.totp_time_calculator() 
    def save_encrypt_OTP_database_controller(self,username,passwd,uri,mailOrUser,plataform):
        self._totpListModel.encrypt_uri(uri=uri,passwd=passwd,username=username,plataform=plataform,mailOrUser=mailOrUser)
    def pre_settings_totpView_controller(self,username,password):
        return self._totpListModel.pre_settings_totpListView(username=username,password=password)
    def totp_remove_item(self,kid):
        self._totpListModel.totp_remove(kid=kid)
    def totp_last_kid_controller(self):
        return self._totpListModel.totp_last_KID()
if __name__ == "__main__":
    app = Controller()
    app.run()
   
