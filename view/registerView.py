
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import messagebox
TITLE_FONT = ("Helvetica", 18, "bold")
LABEL_FONT = ("Helvetica", 12)
BUTTON_FONT = ("Helvetica", 12)
LINK_FONT = ("Helvetica", 10, "underline")
class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#f4f4f4")
        self.controller = controller
        label = tk.Label(self, text="Register Page", font=TITLE_FONT, bg="#f4f4f4", fg="#333")
        label.pack(side="top", fill="x", pady=10)

        tk.Label(self, text="Username:", font=LABEL_FONT, bg="#f4f4f4", fg="#333").pack(pady=5)
        username_entry = tk.Entry(self, font=LABEL_FONT)
        username_entry.pack(pady=5)


        tk.Label(self, text="Password:", font=LABEL_FONT, bg="#f4f4f4", fg="#333").pack(pady=5)
        password_entry = tk.Entry(self, show="*", font=LABEL_FONT)
        password_entry.pack(pady=5)

        tk.Label(self, text="Confirm Password:", font=LABEL_FONT, bg="#f4f4f4", fg="#333").pack(pady=5)
        confirm_password_entry = tk.Entry(self, show="*", font=LABEL_FONT)
        confirm_password_entry.pack(pady=5)

        register_button = tk.Button(self, text="Register", font=BUTTON_FONT, bg="#4CAF50", fg="white", command=lambda: self.register(username_entry, password_entry, confirm_password_entry))
        register_button.pack(pady=10)

        back_link = tk.Label(self, text="Back to Login", font=LINK_FONT, fg="#007BFF", bg="#f4f4f4", cursor="hand2")
        back_link.pack(pady=10)
        back_link.bind("<Button-1>", lambda e: controller.show_frame("LoginPage"))

    def register(self, username_entry, password_entry, confirm_password_entry):
        username = username_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()

        if not username or not password or not confirm_password:
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        if password != confirm_password:
            messagebox.showerror("Password Error", "Passwords do not match.")
            return
        
        register_status = self.controller.register_user_controller(username=username,password=password)
        if register_status == 1:
            messagebox.showinfo("Registration Success", f"Account created for {username}!")
            self.controller.show_frame("LoginPage")
        else:
            messagebox.showerror("Duplicate error","This user already exists")
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        confirm_password_entry.delete(0, tk.END)