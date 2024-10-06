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
        popup.title("Aviso!")
        mensagem = ctk.CTkLabel(popup, text=mensagem, text_color=cor_mensagem, font=('system', 20))
        mensagem.pack(padx=40, pady=30)
        botao_fechar = ctk.CTkButton(popup, text='Fechar', fg_color='#00bf63', text_color='white', command=popup.destroy)
        botao_fechar.pack(padx=40, pady=(0, 30))
