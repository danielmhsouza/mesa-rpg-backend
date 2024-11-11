from typing import List, Dict, Any
import mysql.connector

class Database:

    _hostname: str = 'hostname'
    _password: str = 'password'
    _db_name: str = 'db_name'
    _user: str = "user"

    db = mysql.connector.connect(
                host= _hostname,
                user= _user,
                password= _password,
                database= _db_name
            )

    def _execute_query(query: str, values:str="") -> bool:
        mycursor = Database.db.cursor()
        
        if values != "":
            mycursor.execute(query, values)
            Database.db.commit()
            return True
        
        mycursor.execute(query, values)
        return True
    
    def _execute_select_query(query: str) -> list:
        mycursor = Database.db.cursor()

        mycursor.execute(query)
        return mycursor.fetchall()

    @staticmethod
    def insert_character(character: List[Any]) -> int:
        """
        Insere um personagem no banco de dados.
        :param character: Lista contendo informações sobre o personagem.
        :return: Um código identificador do personagem inserido.
        """
        # Lógica para inserir um personagem no banco de dados
        return 1

    @staticmethod
    def update_entry_campaign_user(code: int):
        """
        Atualiza a entrada de campanha do usuário no banco de dados.
        :param code: Código da campanha a ser atualizado.
        """
        # Lógica para atualizar a entrada da campanha do usuário
        pass

    @staticmethod
    def select_user(email: str, password: str) -> Dict[str, Any]:
        """
        Seleciona um usuário do banco de dados com base no e-mail e senha fornecidos.
        :param email: E-mail do usuário.
        :param password: Senha do usuário.
        :return: Dicionário contendo informações do usuário.
        """
        # Lógica para selecionar um usuário do banco de dados
        return {}

    @staticmethod
    def update_user_characters(character_code: int):
        """
        Atualiza os personagens do usuário no banco de dados.
        :param character_code: Código do personagem a ser atualizado.
        """
        # Lógica para atualizar os personagens do usuário
        pass

    @staticmethod
    def create_campaign(name: str, desc: str, freq: str, img_link: str, id_user: int) -> int:
        """
        Cria uma nova campanha no banco de dados.
        :param name: Nome da campanha.
        :param desc: Descrição da campanha.
        :param freq: Frequência da campanha.
        :param img_link: Link para a imagem da campanha.
        :param id_user: ID do usuário que cria a campanha.
        :return: Um código identificador da campanha criada.
        """
        # Lógica para criar uma nova campanha no banco de dados
        return 1

    @staticmethod
    def select_campaign_data(code: int) -> Dict[str, Any]:
        """
        Seleciona os dados de uma campanha do banco de dados com base no código fornecido.
        :param code: Código da campanha.
        :return: Dicionário contendo dados da campanha.
        """
        # Lógica para selecionar os dados da campanha do banco de dados
        return {}
