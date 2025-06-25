import tkinter as tk
from tkinter import simpledialog, messagebox

TITLE_FONT = ("Helvetica", 18, "bold")
LABEL_FONT = ("Helvetica", 11)
BUTTON_FONT = ("Helvetica", 12)
LINK_FONT = ("Helvetica", 10, "underline")

class TotpPage(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        
        tk.Frame.__init__(self, parent, bg="#f4f4f4")
        

        self.tokens = []
        
        top_bar = tk.Frame(self, bg="#f4f4f4")
        top_bar.pack(side="top", fill="x", pady=5)

        add_button = tk.Button(top_bar, text="Adicionar", font=BUTTON_FONT, bg="#4CAF50", fg="white", command=self.add_token)
        add_button.pack(side="left", padx=5)

       
        self.canvas = tk.Canvas(self, bg="#f4f4f4", highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        
        self.token_container = tk.Frame(self.canvas, bg="#f4f4f4")
        self.canvas.create_window((0, 0), window=self.token_container, anchor="nw")

        
        self.token_container.bind("<Configure>", self.on_frame_configure)

        self.update_timer()

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def load_token(self,totps_list):
        if totps_list != None:
            for totp_dict in totps_list:
                kid = totp_dict["kid"]
            
                uri = totp_dict["uri"]
                plataform = totp_dict["plataform"]
                emailOrUser = totp_dict["emailOrUser"]
                totp_number = self.controller.totp_number_controller(uri)
                self._creating_ballons(kid=kid,platform=plataform,user=emailOrUser,uri=uri,totp_number=totp_number)

    def add_token(self):
        platform = simpledialog.askstring("Plataforma", "Digite a plataforma:")
        user = simpledialog.askstring("Usuário/Email", "Digite o usuário ou email:")
        uri = simpledialog.askstring("URI", "Cole a URI do TOTP (otpauth://...):")

        if not (platform and user and uri):
            messagebox.showwarning("Dados incompletos", "Por favor, preencha todos os campos.")
            return

        try:
            totp_number = self.controller.totp_number_controller(uri)
            
        except Exception as e:
            messagebox.showerror("Erro", f"URI inválida.\nDetalhes: {e}")
            return

        self.controller.save_encrypt_OTP_database_controller(
            username=self.controller.username,
            passwd=self.controller.password,
            uri=uri,
            mailOrUser=user,
            plataform=platform)
        
        kid =self.controller.totp_last_kid_controller()
        self._creating_ballons(kid=kid,platform=platform,user=user,totp_number=totp_number,uri=uri)

        
    def _creating_ballons(self,kid,platform,user,totp_number,uri):
        token_frame = tk.Frame(self.token_container, bg="white", bd=2, relief="groove", padx=10, pady=5)
        token_frame.pack(pady=5, fill="x")

        title = tk.Label(token_frame, text=f"{platform} - {user}", font=LABEL_FONT, bg="white", fg="#333")
        title.pack(anchor="w")

        totp_code = tk.Label(token_frame, text=totp_number, font=("Helvetica", 24, "bold"), fg="#4CAF50", bg="white")
        totp_code.pack(side="left", padx=5, pady=5)

        circle_canvas = tk.Canvas(token_frame, width=30, height=30, bg="white", highlightthickness=0)
        circle_canvas.pack(side="left", padx=5)
        arc = circle_canvas.create_arc((2, 2, 28, 28), start=0, extent=0, fill="#4CAF50")
        remove_button = tk.Button(token_frame, 
                                  text="Delete", 
                                  font=("Helvetica", 8), 
                                  bg="#ff4d4d", 
                                  fg="white",
                                  command=lambda: self._remove_token_by_frame(token_frame))
        remove_button.pack(side="left", padx=5)
        

        self.tokens.append({
            "kid":kid,
            "frame": token_frame,
            "code_label": totp_code,
            "canvas": circle_canvas,
            "arc": arc,
            "uri": uri
        })
    def update_timer(self):
        for token in self.tokens:
            remaining = self.controller.totp_time_controller()
            extent = (remaining / 30) * 360
            token["canvas"].itemconfig(token["arc"], extent=extent)
            if remaining == 30:
                token["code_label"].config(text=self.controller.totp_number_controller(token["uri"]))
        self.after(1000, self.update_timer)

    def _remove_token_by_frame(self, frame):
        
        for i, token in enumerate(self.tokens):
            
            if token["frame"] == frame:
                frame.destroy()
                self.controller.totp_remove_item(kid=token["kid"])
                self.tokens.pop(i)
                break
            
