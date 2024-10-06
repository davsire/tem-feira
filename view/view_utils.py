import customtkinter as ctk
from tkintermapview import TkinterMapView


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
    def abrir_popup_mapa():

        def add_marker_event(coords):
            latitude, longitude = coords
            mapa.delete_all_marker()
            mapa.set_marker(latitude, longitude, text="Sua feira")
            print(f'Coordenadas: lat {latitude}, long {longitude}')

        popup = ctk.CTkToplevel()
        popup.title("Localização")
        popup.geometry("800x600")
        label_popup = ctk.CTkLabel(popup, text="Selecione sua localização", font=('system', 24))
        label_popup.pack(pady=20, padx=20)

        mapa = TkinterMapView(popup, width=400, height=400, corner_radius=0)
        mapa.pack(fill="both", expand=True)
        mapa.set_position(-27.595378, -48.548050)  # Coordenadas de Florianópolis
        mapa.set_zoom(12)
        mapa.add_left_click_map_command(add_marker_event)

        botao_fechar = ctk.CTkButton(popup, text="Fechar", fg_color='#00bf63', text_color='white', command=popup.destroy)
        botao_fechar.pack(pady=10)
