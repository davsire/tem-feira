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
