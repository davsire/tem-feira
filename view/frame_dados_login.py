import customtkinter as ctk


class FrameDadosLogin(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color='white')
        for i in range(4):
            self.grid_rowconfigure(i, weight=i%2)
        self.grid_columnconfigure(0, weight=1)

        self.email_label = ctk.CTkLabel(self, text='E-mail', font=('system', 20))
        self.email_entry = ctk.CTkEntry(self, height=50, placeholder_text='Digite seu e-mail')
        self.email_label.grid(row=0, column=0, sticky='w')
        self.email_entry.grid(row=1, column=0, pady=(0,20), sticky='new')

        self.senha_label = ctk.CTkLabel(self, text='Senha', font=('system', 20))
        self.senha_entry = ctk.CTkEntry(self, height=50, placeholder_text='Digite sua senha', show='*')
        self.senha_label.grid(row=2, column=0, sticky='w')
        self.senha_entry.grid(row=3, column=0, sticky='new')
