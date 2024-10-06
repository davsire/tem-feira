from controller.controller_feirante import ControllerFeirante
from exception.campo_obrigatorio_exception import CampoObrigatorioException
from model.feirante import Feirante
from model.usuario import TipoUsuario
from view.view_main import ViewMain
from view.view_utils import ViewUtils


class ControllerMain:
    __instancia = None

    def __init__(self):
        self.__usuario_logado: Feirante | None = None
        self.__tipo_usuario_logado: TipoUsuario | None = None
        self.__controller_feirante = ControllerFeirante()
        self.__app = ViewMain(self)

    def __new__(cls):
        if ControllerMain.__instancia is None:
            ControllerMain.__instancia = object.__new__(cls)
        return ControllerMain.__instancia

    @property
    def usuario_logado(self):
        return self.__usuario_logado

    @property
    def tipo_usuario_logado(self):
        return self.__tipo_usuario_logado

    def iniciar_app(self):
        self.__app.mainloop()

    def cadastrar_usuario(self, dados, tipo: TipoUsuario):
        try:
            usuario = None
            if tipo == TipoUsuario.FEIRANTE:
                usuario = self.__controller_feirante.cadastrar_feirante(dados)
            if tipo == TipoUsuario.CLIENTE:
                pass
            if usuario:
                self.__usuario_logado = usuario
                self.__tipo_usuario_logado = tipo
                self.__app.alternar_telas('base')
        except CampoObrigatorioException as e:
            ViewUtils.abrir_popup_mensagem(str(e), 'red')

    def excluir_conta(self):
        if self.__tipo_usuario_logado == TipoUsuario.FEIRANTE:
            self.__controller_feirante.excluir_feirante(self.__usuario_logado)
        if self.__tipo_usuario_logado == TipoUsuario.CLIENTE:
            pass
        self.__tipo_usuario_logado = None
        self.__tipo_usuario_logado = None
        self.__app.alternar_telas('login_cadastro')
