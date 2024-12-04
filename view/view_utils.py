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
        popup.attributes('-topmost', True)
        popup.configure(fg_color='white')
        popup.title("Aviso!")
        mensagem = ctk.CTkLabel(popup, text=mensagem, text_color=cor_mensagem, font=('system', 20))
        mensagem.pack(padx=40, pady=30)
        botao_fechar = ctk.CTkButton(popup, text='Fechar', fg_color='#00bf63', text_color='white', command=popup.destroy)
        botao_fechar.pack(padx=40, pady=(0, 30))

    @staticmethod
    def abrir_popup_confirmacao(mensagem: str, texto_acao: str, acao, cor_botao_acao: str = '#00bf63'):
        popup = ctk.CTkToplevel()
        popup.attributes('-topmost', True)
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


    @staticmethod
    def abrir_popup_input(mensagem: str, texto_acao: str, acao, mensagem_erro, cor_botao_acao: str = '#00bf63'):
        popup = ctk.CTkToplevel()
        popup.attributes('-topmost', True)
        popup.configure(fg_color='white')
        popup.title("Input")
        
        label_mensagem = ctk.CTkLabel(popup, text=mensagem, text_color='black', font=('system', 20))
        label_mensagem.pack(padx=40, pady=(20, 10))
        
        input = ctk.CTkEntry(popup, width=250)
        input.pack(padx=40, pady=(0, 20))
        
        botao_cancelar = ctk.CTkButton(
            popup, text='Cancelar', fg_color='white', text_color='#00bf63',
            command=popup.destroy
        )
        botao_confirmar = ctk.CTkButton(
            popup, text=texto_acao, fg_color=cor_botao_acao, text_color='white',
            command=lambda: (acao_com_input())
        )

        def acao_com_input():
            valor_input = input.get().strip()
            if not valor_input:
                ViewUtils.abrir_popup_mensagem(mensagem_erro, cor_mensagem='red')
            else:
                acao(valor_input)
                popup.destroy()
        
        botao_cancelar.pack(side="left", padx=(50, 0), pady=(0, 30))
        botao_confirmar.pack(side="right", padx=(0, 50), pady=(0, 30))