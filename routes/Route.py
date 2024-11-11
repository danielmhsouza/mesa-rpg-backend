

from typing import List, Dict, Any

from controllers.Controller import Controller

class Route:
    def __init__(self):
        self.controller = Controller()

    def login(self, email: str, password: str) -> Dict[str, Any]:
        """
        Realiza o login do usuário usando o controlador.
        :param email: E-mail do usuário.
        :param password: Senha do usuário.
        :return: Dados do usuário.
        """
        return self.controller.login(email, password)
    def register(self, user_name: str, email: str, password: str, conf_pass: str):
        if conf_pass != password:
            return {
                "statusCode": 403,
                "data": "Confirme a senha corretamente!"
            }
        return self.controller.register(user_name, email, password)

    def enter_campaign(self, code: int, character_code: int) -> bool:
        """
        Adiciona uma entrada de campanha usando o controlador.
        :param code: Código da campanha.
        :param character_code: Lista de códigos de personagens.
        :return: Retorna True se a entrada na campanha for bem-sucedida, False caso contrário.
        """
        return self.controller.insert_entry_campaign(code, character_code)

    def create_campaign(self, name: str, desc: str, freq: str, img_link: str) -> bool:
        """
        Cria uma nova campanha usando o controlador.
        :param name: Nome da campanha.
        :param desc: Descrição da campanha.
        :param freq: Frequência da campanha.
        :param img_link: Link para a imagem da campanha.
        :return: Retorna True se a criação da campanha for bem-sucedida, False caso contrário.
        """
        return self.controller.create_campaign(name, desc, freq, img_link)

    def enter_campaign_as_master(self, code: int, id_user: int) -> Dict[str, Any]:
        """
        Entra em uma campanha como mestre usando o controlador.
        :param code: Código da campanha.
        :param id_user: ID do usuário.
        :return: Dados da campanha e tipo de usuário.
        """
        return self.controller.enter_campaign_as_master(code, id_user)

    def enter_campaign_as_player(self, code: int, id_user: int) -> Dict[str, Any]:
        """
        Entra em uma campanha como jogador usando o controlador.
        :param code: Código da campanha.
        :param id_user: ID do usuário.
        :return: Dados da campanha e tipo de usuário.
        """
        return self.controller.enter_campaign_as_player(code, id_user)

    def create_character(self, data):
        pass