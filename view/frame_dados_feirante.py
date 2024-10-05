import customtkinter as ctk
from model.feirante import FormaContato
from tkintermapview import TkinterMapView


class FrameDadosFeirante(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color='white')
        for i in range(10):
            self.grid_rowconfigure(i, weight=i%2)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=10)

        self.nome_feira_label = ctk.CTkLabel(self, text='Nome da feira', font=('system', 20))
        self.nome_feira_entry = ctk.CTkEntry(self, height=40, placeholder_text='Digite o nome da feira')
        self.nome_feira_label.grid(row=0, column=0, columnspan=2, sticky='w')
        self.nome_feira_entry.grid(row=1, column=0, columnspan=2, sticky='ew')

        self.contato_label = ctk.CTkLabel(self, text='Contato', font=('system', 20))
        self.forma_contato_entry = ctk.CTkComboBox(self, values=[fc.value for fc in FormaContato], width=150, height=40)
        self.contato_entry = ctk.CTkEntry(self, width=150, height=40, placeholder_text='Digite o contato')
        self.contato_label.grid(row=2, column=0, columnspan=2, sticky='w')
        self.forma_contato_entry.grid(row=3, column=0, sticky='ew', padx=(0, 10))
        self.contato_entry.grid(row=3, column=1, sticky='ew', padx=(10, 0))

        self.localizacao_label = ctk.CTkLabel(self, text='Localização', font=('system', 20))
        self.localizacao_entry = ctk.CTkButton(self, height=40, text='Selecione sua localização no mapa', fg_color='#00bf63', text_color='white', command=self.abrir_popup)
        self.localizacao_label.grid(row=4, column=0, columnspan=2, sticky='w')
        self.localizacao_entry.grid(row=5, column=0, columnspan=2, sticky='ew')

        self.email_label = ctk.CTkLabel(self, text='E-mail', font=('system', 20))
        self.email_entry = ctk.CTkEntry(self, height=40, placeholder_text='Digite seu e-mail')
        self.email_label.grid(row=6, column=0, columnspan=2, sticky='w')
        self.email_entry.grid(row=7, column=0, columnspan=2, sticky='ew')

        self.senha_label = ctk.CTkLabel(self, text='Senha', font=('system', 20))
        self.senha_entry = ctk.CTkEntry(self, height=40, placeholder_text='Digite sua senha', show='*')
        self.senha_label.grid(row=8, column=0, columnspan=2, sticky='w')
        self.senha_entry.grid(row=9, column=0, columnspan=2, sticky='ew')

        frame_meio = ctk.CTkFrame(self, corner_radius=10, fg_color="white")
        frame_meio.grid(row=0, rowspan=10, column=2, padx=20, pady=20, sticky="nsew")

        mapa = TkinterMapView(frame_meio, width=400, height=400, corner_radius=0)
        mapa.set_position(-23.55052, -46.633308)
        mapa.set_zoom(12)
        mapa.set_marker(-23.55052, -46.633308, text="São Paulo")
        mapa.pack(fill="both", expand=True)
        mapa.bind("<Button-1>")

    def abrir_popup(self):

        def on_click(event):
            x, y = event.x, event.y
            latitude, longitude = mapa.convert_canvas_coords_to_lat_lon(x, y)
            mapa.set_marker(latitude, longitude, text=f"Coordenadas: {latitude:.5f}, {longitude:.5f}")

        popup = ctk.CTkToplevel(self)
        popup.title("Localização")
        popup.geometry("800x600")
        label_popup = ctk.CTkLabel(popup, text="Selecione sua localização", font=('system', 24))
        label_popup.pack(pady=20, padx=20)

        mapa = TkinterMapView(popup, width=400, height=400, corner_radius=0)
        mapa.set_position(-23.55052, -46.633308)
        mapa.set_zoom(12)
        mapa.set_marker(-23.55052, -46.633308, text="São Paulo")
        mapa.pack(fill="both", expand=True)
        mapa.bind("<Button-1>", on_click)
        botao_fechar = ctk.CTkButton(popup, text="Fechar", fg_color='#00bf63', text_color='white', command=popup.destroy)
        botao_fechar.pack(pady=10)
