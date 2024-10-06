import customtkinter as ctk


class ViewUtils:

    def __init__(self):
        pass

    @staticmethod
    def obter_botao(app, label: str, fg_color: str = '#00bf63', text_color: str = 'white'):
        return ctk.CTkButton(
            app,
            text=label,
            height=40,
            width=50,
            corner_radius=20,
            text_color=text_color,
            fg_color=fg_color,
            font=('system', 24, 'bold')
        )

    @staticmethod
    def abrir_popup_mensagem(mensagem: str, cor_mensagem: str = 'black'):
        popup = ctk.CTkToplevel()
        popup.configure(fg_color='white')
        popup.title("Aviso!")
        mensagem = ctk.CTkLabel(popup, text=mensagem, text_color=cor_mensagem, font=('system', 20))
        mensagem.pack(padx=40, pady=30)
        botao_fechar = ctk.CTkButton(popup, text='Fechar', fg_color='#00bf63', text_color='white', command=popup.destroy)
        botao_fechar.pack(padx=40, pady=(0, 30))

    @staticmethod
    def abrir_popup_confirmacao(mensagem: str, texto_acao: str, acao, cor_botao_acao: str = '#00bf63'):
        popup = ctk.CTkToplevel()
        popup.configure(fg_color='white')
        popup.title("Confirmar ação")
        mensagem = ctk.CTkLabel(popup, text=mensagem, text_color='black', font=('system', 20))
        mensagem.pack(padx=40, pady=30)
        botao_cancelar = ctk.CTkButton(
            popup, command=popup.destroy,
            text='Cancelar', fg_color='white', text_color='#00bf63'
        )
        botao_acao = ctk.CTkButton(
            popup, command=lambda: (acao(), popup.destroy()),
            text=texto_acao, fg_color=cor_botao_acao, text_color='white'
        )
        botao_cancelar.pack(side="left", padx=(50, 0), pady=(0, 30))
        botao_acao.pack(side="right", padx=(0, 50), pady=(0, 30))
