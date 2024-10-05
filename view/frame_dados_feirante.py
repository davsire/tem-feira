import customtkinter as ctk
from tkintermapview import TkinterMapView
from model.dia_funcionamento import DiaSemana
from model.feirante import FormaContato


class FrameDiaFuncionamento(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color='white')
        for i in range(9):
            self.grid_rowconfigure(i, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.label_dias_funcionamento = ctk.CTkLabel(self, text='Dias de funcionamento', text_color='black', font=('system', 22))
        self.label_dias_funcionamento.grid(row=0, column=0, columnspan=3, pady=(0, 15), sticky='ew')

        self.label_abertura = ctk.CTkLabel(self, text='Abertura', text_color='black', font=('system', 16))
        self.label_abertura.grid(row=1, column=1, pady=(0, 5))
        self.label_fechamento = ctk.CTkLabel(self, text='Fechamento', text_color='black', font=('system', 16))
        self.label_fechamento.grid(row=1, column=2, pady=(0, 5))

        for idx, dia_semana in enumerate(DiaSemana):
            var = ctk.CTkCheckBox(self, text=dia_semana.value, fg_color='#00bf63')
            var_abertura = ctk.CTkEntry(self, height=40, placeholder_text='HH:mm')
            var_fechamento = ctk.CTkEntry(self, height=40, placeholder_text='HH:mm')
            var.grid(row=idx+2, column=0, sticky='w', pady=10)
            var_abertura.grid(row=idx+2, column=1, sticky='w', pady=10)
            var_fechamento.grid(row=idx+2, column=2, sticky='w', pady=10)


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
        self.nome_feira_entry.grid(row=1, column=0, columnspan=2, sticky='new')

        self.contato_label = ctk.CTkLabel(self, text='Contato', font=('system', 20))
        self.forma_contato_entry = ctk.CTkComboBox(self, values=[fc.value for fc in FormaContato], width=150, height=40)
        self.contato_entry = ctk.CTkEntry(self, width=150, height=40, placeholder_text='Digite o contato')
        self.contato_label.grid(row=2, column=0, columnspan=2, sticky='w')
        self.forma_contato_entry.grid(row=3, column=0, sticky='new', padx=(0, 10))
        self.contato_entry.grid(row=3, column=1, sticky='new', padx=(10, 0))

        self.localizacao_label = ctk.CTkLabel(self, text='Localização', font=('system', 20))
        self.localizacao_entry = ctk.CTkButton(self, height=40, text='Selecione sua localização no mapa', fg_color='#00bf63', text_color='white', command=self.abrir_popup)
        self.localizacao_label.grid(row=4, column=0, columnspan=2, sticky='w')
        self.localizacao_entry.grid(row=5, column=0, columnspan=2, sticky='new')

        self.email_label = ctk.CTkLabel(self, text='E-mail', font=('system', 20))
        self.email_entry = ctk.CTkEntry(self, height=40, placeholder_text='Digite seu e-mail')
        self.email_label.grid(row=6, column=0, columnspan=2, sticky='w')
        self.email_entry.grid(row=7, column=0, columnspan=2, sticky='new')

        self.senha_label = ctk.CTkLabel(self, text='Senha', font=('system', 20))
        self.senha_entry = ctk.CTkEntry(self, height=40, placeholder_text='Digite sua senha', show='*')
        self.senha_label.grid(row=8, column=0, columnspan=2, sticky='w')
        self.senha_entry.grid(row=9, column=0, columnspan=2, sticky='new')

        self.dias_funcionamento = FrameDiaFuncionamento(self)
        self.dias_funcionamento.grid(column=2, row=0, rowspan=10, padx=30, sticky='ew')

    def abrir_popup(self):

        def on_click(event):
            x, y = event.x, event.y
            latitude, longitude = mapa.convert_canvas_coords_to_lat_lon(x, y)
            mapa.set_marker(latitude, longitude, text=f"Coordenadas: {latitude:.5f}, {longitude:.5f}")


        def add_marker_event(coords):
            print("Coordenadas:", coords)
            new_marker = mapa.set_marker(coords[0], coords[1], text="Feira")

        popup = ctk.CTkToplevel(self)
        popup.title("Localização")
        popup.geometry("800x600")
        label_popup = ctk.CTkLabel(popup, text="Selecione sua localização", font=('system', 24))
        label_popup.pack(pady=20, padx=20)

        mapa = TkinterMapView(popup, width=400, height=400, corner_radius=0)
        mapa.set_position(-27.595378, -48.548050)  # Coordenadas de Florianópolis
        mapa.set_zoom(12)


        mapa.pack(fill="both", expand=True)
        mapa.bind("<Button-1>", on_click)

        # Adiciona o comando de clique direito para adicionar marcador
        mapa.add_right_click_menu_command(label="Adicionar Marcador",
                                        command=add_marker_event,
                                        pass_coords=True)

        botao_fechar = ctk.CTkButton(popup, text="Fechar", fg_color='#00bf63', text_color='white', command=popup.destroy)
        botao_fechar.pack(pady=10)
