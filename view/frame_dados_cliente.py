from datetime import datetime
import customtkinter as ctk
from tkintermapview import TkinterMapView
import tkcalendar as tkcal
from model.cliente import Cliente


class FrameDadosCliente(ctk.CTkFrame):

    def __init__(self, master, cliente_logado: Cliente | None):
        super().__init__(master)
        self.configure(fg_color='white')
        self.__latitude = None
        self.__longitude = None
        self.__data_nascimento = None

        for i in range(10):
            self.grid_rowconfigure(i, weight=i % 2)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.nome_label = ctk.CTkLabel(self, text='Nome *', font=('system', 20))
        self.nome_entry = ctk.CTkEntry(self, height=40, placeholder_text='Digite seu nome')
        self.nome_label.grid(row=0, column=1, sticky='w')
        self.nome_entry.grid(row=1, column=1, sticky='new')

        self.data_nascimento_label = ctk.CTkLabel(self, text='Data de Nascimento *', font=('system', 20))
        self.data_nascimento_button = ctk.CTkButton(
            self, height=40, text='Selecione a data',
            fg_color='#00bf63', text_color='white',
            command=self.abrir_calendario
        )
        self.data_nascimento_label.grid(row=2, column=1, sticky='w')
        self.data_nascimento_button.grid(row=3, column=1, sticky='new')

        self.localizacao_label = ctk.CTkLabel(self, text='Localização *', font=('system', 20))
        self.localizacao_entry = ctk.CTkButton(
            self, height=40, text='Selecione sua localização no mapa',
            fg_color='#00bf63', text_color='white',
            command=self.abrir_popup_mapa
        )
        self.localizacao_label.grid(row=4, column=1, sticky='w')
        self.localizacao_entry.grid(row=5, column=1, sticky='new')

        self.email_label = ctk.CTkLabel(self, text='E-mail *', font=('system', 20))
        self.email_entry = ctk.CTkEntry(self, height=40, placeholder_text='Digite seu e-mail')
        self.email_label.grid(row=6, column=1, sticky='w')
        self.email_entry.grid(row=7, column=1, sticky='new')

        self.senha_label = ctk.CTkLabel(self, text='Senha *', font=('system', 20))
        self.senha_entry = ctk.CTkEntry(self, height=40, placeholder_text='Digite sua senha', show='*')
        self.senha_label.grid(row=8, column=1, sticky='w')
        self.senha_entry.grid(row=9, column=1, sticky='new')
        
        if cliente_logado:
            self.__preencher_dados_edicao(cliente_logado)
        
    def abrir_popup_mapa(self):

        def adicionar_marcador(coords):
            self.__latitude, self.__longitude = coords
            mapa.delete_all_marker()
            mapa.set_marker(self.__latitude, self.__longitude, text="Sua casa")
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

        if self.__latitude and self.__longitude:
            adicionar_marcador((self.__latitude, self.__longitude))
            mapa.set_position(self.__latitude, self.__longitude)

        botao_fechar = ctk.CTkButton(popup, text="Confirmar", fg_color='#00bf63', text_color='white', command=popup.destroy)
        botao_fechar.pack(pady=10)

    def abrir_calendario(self):
        
        def selecionar_data():
            data_selecionada = cal.get_date()
            self.__data_nascimento = data_selecionada
            self.data_nascimento_button.configure(text=data_selecionada)
            popup.destroy()

        popup = ctk.CTkToplevel(self)
        popup.attributes('-topmost', True)
        popup.title("Calendário")
        popup.geometry("500x500")
        cal = tkcal.Calendar(popup, selectmode='day', date_pattern='dd/mm/yyyy', year=2000, month=6, maxdate=datetime.now())
        cal.pack(pady=40, padx=40, expand=True, fill='both')

        botao_selecao = ctk.CTkButton(popup, text="Selecionar", fg_color='#00bf63', text_color='white', command=selecionar_data)
        botao_selecao.pack(pady=20)

    def obter_dados_cliente(self):
        return {
            'nome': self.nome_entry.get(),
            'data_nascimento': self.__data_nascimento,
            'localizacao': {
                'latitude': self.__latitude,
                'longitude': self.__longitude,
            },
            'email': self.email_entry.get(),
            'senha': self.senha_entry.get()
        }

    def __preencher_dados_edicao(self, cliente_logado: Cliente):
        self.nome_entry.insert(0, cliente_logado.nome)
        self.__data_nascimento = cliente_logado.data_nascimento
        self.data_nascimento_button.configure(text=cliente_logado.data_nascimento)
        self.__latitude = cliente_logado.localizacao.latitude
        self.__longitude = cliente_logado.localizacao.longitude
        self.localizacao_entry.configure(text=f'Coordenadas: lat {self.__latitude:.3f}, lng {self.__longitude:.3f}')
        self.email_entry.insert(0, cliente_logado.email)
