
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import tkinter as tk
from tkinter import messagebox
TITLE_FONT = ("Helvetica", 18, "bold")
LABEL_FONT = ("Helvetica", 12)
BUTTON_FONT = ("Helvetica", 12)
LINK_FONT = ("Helvetica", 10, "underline")
class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#f4f4f4")
        self.controller = controller
        label = tk.Label(self, text="Login Page", font=TITLE_FONT, bg="#f4f4f4", fg="#333")
        label.pack(side="top", fill="x", pady=10)

        tk.Label(self, text="Username:", font=LABEL_FONT, bg="#f4f4f4", fg="#333").pack(pady=5)
        username_entry = tk.Entry(self, font=LABEL_FONT)
        username_entry.pack(pady=5)

        tk.Label(self, text="Password:", font=LABEL_FONT, bg="#f4f4f4", fg="#333").pack(pady=5)
        password_entry = tk.Entry(self, show="*", font=LABEL_FONT)
        password_entry.pack(pady=5)

        login_button = tk.Button(self, text="Login", font=BUTTON_FONT, bg="#4CAF50", fg="white", command=lambda: self.login(username_entry, password_entry))
        login_button.pack(pady=10)

        register_link = tk.Label(self, text="Don't have an account? Register here", font=LINK_FONT, fg="#007BFF", bg="#f4f4f4", cursor="hand2")
        register_link.pack(pady=10)
        register_link.bind("<Button-1>", lambda e: controller.show_frame("RegisterPage"))

    def login(self, username_entry, password_entry):
        username = username_entry.get()
        password = password_entry.get()
        login_auth_status = self.controller.login_user_auth_controller(username=username,password=password)
        if login_auth_status !=1:
            messagebox.showwarning("Login Failed", "Please enter both username and password.")    
        else:
            messagebox.showinfo("Login Success", f"Welcome, {username}!")
            self.controller.username = username
            self.controller.password = password
            self.controller.show_frame("TotpPage")
            totps_list = self.controller.pre_settings_totpView_controller(username=username,password=password)
            self.controller.frames["TotpPage"].load_token(totps_list)
