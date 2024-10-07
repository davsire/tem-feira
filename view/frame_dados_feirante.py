import customtkinter as ctk
from tkintermapview import TkinterMapView
from model.dia_funcionamento import DiaSemana
from model.feirante import FormaContato, Feirante


class FrameDiaFuncionamento(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color='white')
        for i in range(9):
            self.grid_rowconfigure(i, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.map_dias_funcionamento = {}

        self.label_dias_funcionamento = ctk.CTkLabel(self, text='Dias de funcionamento *', text_color='black', font=('system', 22))
        self.label_dias_funcionamento.grid(row=0, column=0, columnspan=3, pady=(0, 15), sticky='ew')

        self.label_abertura = ctk.CTkLabel(self, text='Abertura', text_color='black', font=('system', 16))
        self.label_abertura.grid(row=1, column=1, pady=(0, 5))
        self.label_fechamento = ctk.CTkLabel(self, text='Fechamento', text_color='black', font=('system', 16))
        self.label_fechamento.grid(row=1, column=2, pady=(0, 5))

        for idx, dia_semana in enumerate(DiaSemana):
            self.map_dias_funcionamento[dia_semana.name] = ctk.CTkCheckBox(self, text=dia_semana.value, fg_color='#00bf63')
            self.map_dias_funcionamento[dia_semana.name + '_abertura'] = ctk.CTkEntry(self, height=40, placeholder_text='HH:mm')
            self.map_dias_funcionamento[dia_semana.name + '_fechamento'] = ctk.CTkEntry(self, height=40, placeholder_text='HH:mm')
            self.map_dias_funcionamento[dia_semana.name].grid(row=idx+2, column=0, sticky='w', pady=10)
            self.map_dias_funcionamento[dia_semana.name + '_abertura'].grid(row=idx+2, column=1, sticky='ew', pady=10, padx=(0, 10))
            self.map_dias_funcionamento[dia_semana.name + '_fechamento'].grid(row=idx+2, column=2, sticky='ew', pady=10)
            self.map_dias_funcionamento[dia_semana.name + '_abertura'].bind('<KeyRelease>', lambda e: self.aplicar_mascara_horario(e))
            self.map_dias_funcionamento[dia_semana.name + '_fechamento'].bind('<KeyRelease>', lambda e: self.aplicar_mascara_horario(e))


    def aplicar_mascara_horario(self, event):
        entry = event.widget
        conteudo = entry.get()
        conteudo = ''.join([char for char in conteudo if char.isdigit()])

        if len(conteudo) >= 3:
            conteudo = conteudo[:2] + ':' + conteudo[2:4]
        elif len(conteudo) > 2:
            conteudo = conteudo[:2] + ':' + conteudo[2:]

        entry.delete(0, ctk.END)
        entry.insert(0, conteudo)

    def obter_dias_funcionamento(self):
        dias_funcionamento = []
        for dia_semana in DiaSemana:
            if self.map_dias_funcionamento[dia_semana.name].get():
                dias_funcionamento.append({
                    'dia_semana': dia_semana.name,
                    'horario_abertura': self.map_dias_funcionamento[dia_semana.name + '_abertura'].get(),
                    'horario_fechamento': self.map_dias_funcionamento[dia_semana.name + '_fechamento'].get(),
                })
        return dias_funcionamento


class FrameDadosFeirante(ctk.CTkFrame):

    def __init__(self, master, feirante_logado: Feirante | None):
        super().__init__(master)
        self.__latitude = None
        self.__longitude = None
        self.configure(fg_color='white')
        for i in range(10):
            self.grid_rowconfigure(i, weight=i%2)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=10)

        self.nome_feira_label = ctk.CTkLabel(self, text='Nome da feira *', font=('system', 20))
        self.nome_feira_entry = ctk.CTkEntry(self, height=40, placeholder_text='Digite o nome da feira')
        self.nome_feira_label.grid(row=0, column=0, columnspan=2, sticky='w')
        self.nome_feira_entry.grid(row=1, column=0, columnspan=2, sticky='new')

        self.contato_label = ctk.CTkLabel(self, text='Contato *', font=('system', 20))
        self.forma_contato_entry = ctk.CTkComboBox(self, values=[fc.value for fc in FormaContato], width=150, height=40)
        self.contato_entry = ctk.CTkEntry(self, width=150, height=40, placeholder_text='Digite o contato')
        self.contato_label.grid(row=2, column=0, columnspan=2, sticky='w')
        self.forma_contato_entry.grid(row=3, column=0, sticky='new', padx=(0, 10))
        self.contato_entry.grid(row=3, column=1, sticky='new', padx=(10, 0))

        self.localizacao_label = ctk.CTkLabel(self, text='Localização *', font=('system', 20))
        self.localizacao_entry = ctk.CTkButton(
            self, height=40, text='Selecione sua localização no mapa',
            fg_color='#00bf63', text_color='white',
            command=self.abrir_popup_mapa
        )
        self.localizacao_label.grid(row=4, column=0, columnspan=2, sticky='w')
        self.localizacao_entry.grid(row=5, column=0, columnspan=2, sticky='new')

        self.email_label = ctk.CTkLabel(self, text='E-mail *', font=('system', 20))
        self.email_entry = ctk.CTkEntry(self, height=40, placeholder_text='Digite seu e-mail')
        self.email_label.grid(row=6, column=0, columnspan=2, sticky='w')
        self.email_entry.grid(row=7, column=0, columnspan=2, sticky='new')

        self.senha_label = ctk.CTkLabel(self, text='Senha *', font=('system', 20))
        self.senha_entry = ctk.CTkEntry(self, height=40, placeholder_text='Digite sua senha', show='*')
        self.senha_label.grid(row=8, column=0, columnspan=2, sticky='w')
        self.senha_entry.grid(row=9, column=0, columnspan=2, sticky='new')

        self.dias_funcionamento = FrameDiaFuncionamento(self)
        self.dias_funcionamento.grid(column=2, row=0, rowspan=10, padx=30, sticky='ew')

        if feirante_logado:
            self.__preencher_dados_edicao(feirante_logado)

    def abrir_popup_mapa(self):

        def adicionar_marcador(coords):
            self.__latitude, self.__longitude = coords
            mapa.delete_all_marker()
            mapa.set_marker(self.__latitude, self.__longitude, text="Sua feira")
            self.localizacao_entry.configure(text=f'Coordenadas: lat {self.__latitude:.3f}, lng {self.__longitude:.3f}')

        popup = ctk.CTkToplevel(self)
        popup.attributes('-topmost', True)
        popup.title("Localização")
        popup.geometry("800x600")
        label_popup = ctk.CTkLabel(popup, text="Selecione sua localização", font=('system', 24))
        label_popup.pack(pady=20, padx=20)

        mapa = TkinterMapView(popup, width=400, height=400, corner_radius=0)
        mapa.pack(fill="both", expand=True)
        mapa.set_position(-27.595378, -48.548050) # Coordenadas de Florianópolis
        mapa.set_zoom(12)
        mapa.add_left_click_map_command(adicionar_marcador)

        botao_fechar = ctk.CTkButton(popup, text="Confirmar", fg_color='#00bf63', text_color='white', command=popup.destroy)
        botao_fechar.pack(pady=10)

    def obter_dados_feirante(self):
        return {
            'email': self.email_entry.get(),
            'senha': self.senha_entry.get(),
            'nome_feira': self.nome_feira_entry.get(),
            'forma_contato': self.forma_contato_entry.get(),
            'contato': self.contato_entry.get(),
            'localizacao': {
                'latitude': self.__latitude,
                'longitude': self.__longitude,
            },
            'dias_funcionamento': self.dias_funcionamento.obter_dias_funcionamento()
        }

    def __preencher_dados_edicao(self, feirante_logado: Feirante):
        self.nome_feira_entry.insert(0, feirante_logado.nome_feira)
        self.forma_contato_entry.set(feirante_logado.forma_contato.name)
        self.contato_entry.insert(0, feirante_logado.contato)
        self.email_entry.insert(0, feirante_logado.email)
        self.__latitude = feirante_logado.localizacao.latitude
        self.__longitude = feirante_logado.localizacao.longitude
        self.localizacao_entry.configure(text=f'Coordenadas: lat {self.__latitude:.3f}, lng {self.__longitude:.3f}')
        for dia_funcionamento in feirante_logado.dias_funcionamento:
            dia_semana = dia_funcionamento.dia_semana.name
            self.dias_funcionamento.map_dias_funcionamento[dia_semana].select()
            self.dias_funcionamento.map_dias_funcionamento[dia_semana + '_abertura'].insert(0, dia_funcionamento.horario_abertura)
            self.dias_funcionamento.map_dias_funcionamento[dia_semana + '_fechamento'].insert(0, dia_funcionamento.horario_fechamento)
