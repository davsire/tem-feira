from tkinter import *
import customtkinter
from PIL import Image
from tkintermapview import TkinterMapView

customtkinter.set_appearance_mode("light")
root = customtkinter.CTk()

root.geometry("1200x800")
root.title("Cadastro de Cliente")
root.configure(bg="white")

# Configurar grid da janela principal
root.grid_columnconfigure(0, weight=2)
root.grid_columnconfigure(1, weight=2)
root.grid_columnconfigure(2, weight=1)
root.grid_rowconfigure(0, weight=1)

# Frames
frame_esquerda = customtkinter.CTkFrame(root, corner_radius=10, fg_color="white")
frame_esquerda.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

frame_meio = customtkinter.CTkFrame(root, corner_radius=10, fg_color="white")
frame_meio.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

frame_direita = customtkinter.CTkFrame(root, corner_radius=10, fg_color="white")
frame_direita.grid(row=0, column=2, padx=20, pady=20, sticky="nsew")

# Configurar grid do frame esquerdo
frame_esquerda.grid_columnconfigure(0, weight=1)
frame_esquerda.grid_columnconfigure(1, weight=1)
frame_esquerda.grid_rowconfigure(0, weight=1)
frame_esquerda.grid_rowconfigure(1, weight=1)
frame_esquerda.grid_rowconfigure(2, weight=1)
frame_esquerda.grid_rowconfigure(3, weight=1)
frame_esquerda.grid_rowconfigure(4, weight=1)
frame_esquerda.grid_rowconfigure(5, weight=1)
frame_esquerda.grid_rowconfigure(6, weight=1)
frame_esquerda.grid_rowconfigure(7, weight=1)
frame_esquerda.grid_rowconfigure(8, weight=1)
frame_esquerda.grid_rowconfigure(9, weight=1)

# Título no frame esquerdo
title_label = customtkinter.CTkLabel(frame_esquerda, text="Cadastro de Cliente", font=("Arial", 16))
title_label.grid(row=0, column=0, columnspan=2, pady=5, sticky="ew")

# Função para alternar entre cadastros
def alternar_cadastro(tipo):
    if tipo == "cliente":
        title_label.configure(text="Cadastro de Cliente")
        data_nascimento_label.grid(row=3, column=0, sticky="e", pady=1, padx=2)
        data_nascimento_entry.grid(row=3, column=1, pady=1, padx=2, sticky="ew")
        localizacao_label.grid(row=4, column=0, sticky="e", pady=1, padx=2)
        localizacao_entry.grid(row=4, column=1, pady=1, padx=2, sticky="ew")
        email_label.grid(row=5, column=0, sticky="e", pady=1, padx=2)
        email_entry.grid(row=5, column=1, pady=1, padx=2, sticky="ew")
        senha_label.grid(row=6, column=0, sticky="e", pady=1, padx=2)
        senha_entry.grid(row=6, column=1, pady=1, padx=2, sticky="ew")
        cadastrar_button.grid(row=7, column=0, columnspan=2, pady=10, padx=10, sticky="ew")
        
        # Centralize the labels and entries
        frame_esquerda.grid_columnconfigure(0, weight=1)
        frame_esquerda.grid_columnconfigure(1, weight=1)
        frame_esquerda.grid_rowconfigure(3, weight=1)
        frame_esquerda.grid_rowconfigure(4, weight=1)
        frame_esquerda.grid_rowconfigure(5, weight=1)
        frame_esquerda.grid_rowconfigure(6, weight=1)
        frame_esquerda.grid_rowconfigure(7, weight=1)
        
    elif tipo == "feirante":
        title_label.configure(text="Cadastro de Feirante")
        data_nascimento_label.grid_forget()
        data_nascimento_entry.grid_forget()
        localizacao_label.grid_forget()
        localizacao_entry.grid_forget()
        email_label.grid(row=3, column=0, sticky="e", pady=1, padx=2)
        email_entry.grid(row=3, column=1, pady=1, padx=2, sticky="ew")
        senha_label.grid(row=4, column=0, sticky="e", pady=1, padx=2)
        senha_entry.grid(row=4, column=1, pady=1, padx=2, sticky="ew")
        cadastrar_button.grid(row=5, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

# Botões para alternar entre cadastros
cliente_button = customtkinter.CTkButton(
    frame_esquerda, 
    text="Cliente", 
    fg_color="green", 
    width=150, 
    height=60, 
    corner_radius=20,  # Tornar o botão mais redondo
    font=("Arial", 14, "bold"),  # Aumentar o tamanho da letra e colocar em negrito
    command=lambda: alternar_cadastro("cliente")
)
cliente_button.grid(row=1, column=0, pady=2, padx=2)  # Reduzir o padding

feirante_button = customtkinter.CTkButton(
    frame_esquerda, 
    text="Feirante", 
    fg_color="green", 
    width=150, 
    height=60, 
    corner_radius=20,  # Tornar o botão mais redondo
    font=("Arial", 14, "bold"),  # Aumentar o tamanho da letra e colocar em negrito
    command=lambda: alternar_cadastro("feirante")
)
feirante_button.grid(row=1, column=1, pady=2, padx=2)  # Reduzir o padding

# Função para abrir o mapa interativo no frame do meio
def abrir_mapa():
    # Cria o mapa centrado em Florianópolis
    map_widget = TkinterMapView(frame_meio, width=800, height=600, corner_radius=0)
    map_widget.set_position(-27.5954, -48.5480)  # Coordenadas de Florianópolis
    map_widget.set_zoom(12)
    map_widget.pack(fill=BOTH, expand=YES)

    # Função para adicionar um marcador e obter a localização clicada
    def on_click(event):
        if event.num == 3:  # Verifica se o botão direito do mouse foi clicado
            lat, lon = map_widget.get_position()
            map_widget.set_marker(lat, lon, text="Localização Selecionada")
            print(f"Localização selecionada: {lat}, {lon}")

    # Vincula a função de clique ao mapa
    map_widget.bind("<Button-3>", on_click)

# Campos no frame esquerdo
nome_label = customtkinter.CTkLabel(frame_esquerda, text="Nome:")
nome_label.grid(row=2, column=0, sticky="e", pady=1, padx=2)
nome_entry = customtkinter.CTkEntry(frame_esquerda, placeholder_text="Digite seu nome")
nome_entry.grid(row=2, column=1, pady=1, padx=2, sticky="ew")

data_nascimento_label = customtkinter.CTkLabel(frame_esquerda, text="Data de Nascimento:")
data_nascimento_entry = customtkinter.CTkEntry(frame_esquerda, placeholder_text="DD/MM/AAAA")

email_label = customtkinter.CTkLabel(frame_esquerda, text="Email:")
email_entry = customtkinter.CTkEntry(frame_esquerda, placeholder_text="Digite seu email")

senha_label = customtkinter.CTkLabel(frame_esquerda, text="Senha:")
senha_entry = customtkinter.CTkEntry(frame_esquerda, show="*", placeholder_text="Digite sua senha")

localizacao_label = customtkinter.CTkLabel(frame_esquerda, text="Localização:")
localizacao_label.grid(row=6, column=0, sticky="e", pady=1, padx=2)
localizacao_entry = customtkinter.CTkEntry(frame_esquerda, placeholder_text="Digite sua localização")
localizacao_entry.grid(row=6, column=1, pady=1, padx=2, sticky="ew")
localizacao_entry.bind("<Button-1>", lambda e: abrir_mapa())

# Botão Cadastrar
cadastrar_button = customtkinter.CTkButton(
    frame_esquerda, 
    text="Cadastrar", 
    fg_color="green", 
    width=150,  # Ajuste a largura para ser menor
    height=60, 
    corner_radius=20,  # Tornar o botão mais redondo
    font=("Arial", 14, "bold")  # Aumentar o tamanho da letra e colocar em negrito
)
cadastrar_button.grid(row=8, column=0, columnspan=2, pady=10, padx=10)

# Centralizar o botão
frame_esquerda.grid_columnconfigure(0, weight=1)
frame_esquerda.grid_columnconfigure(1, weight=1)

# Função para ir para a tela de login
def ir_para_login(event):
    print("Navegando para a tela de login...")  # Substitua esta linha pelo código para abrir a tela de login

# Label clicável para ir para a tela de login
login_label = customtkinter.CTkLabel(
    frame_esquerda, 
    text="Já Tem Conta? Clique aqui!", 
    text_color="#ADD8E6",  # Azul fraco
    cursor="hand2",
    font=("Arial", 18, "bold")  # Aumentar a fonte e colocar em negrito
)
login_label.grid(row=9, column=0, columnspan=2, pady=5)
login_label.bind("<Button-1>", ir_para_login)

# Carregar e exibir a foto no frame direito
try:
    image_path = "./assets/tem-feira.png"  # Verifique se o caminho está correto
    image = Image.open(image_path)
    photo = customtkinter.CTkImage(light_image=image, dark_image=image, size=(333, 800))  # 1/3 da largura da tela
    image_label = customtkinter.CTkLabel(frame_direita, image=photo)
    image_label.image = photo  # Manter uma referência da imagem
    image_label.grid(row=0, column=0, sticky="nsew")
    frame_direita.grid_rowconfigure(0, weight=1)
    frame_direita.grid_columnconfigure(0, weight=1)
except Exception as e:
    print(f"Erro ao carregar a imagem: {e}")

# Inicializar com o cadastro de cliente
alternar_cadastro("cliente")

root.mainloop()