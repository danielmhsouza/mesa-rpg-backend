from typing import List, Dict, Any
from models.User import User
from models.Campaign import Campaign
from models.Master import Master
from models.Artifact import Artifact
from models.Database import Database

class Controller:
    def __init__(self):
        self.user = None
        self.campaign = None
        self.master = None

    def login(self, email: str, password: str) -> Dict[str, Any]:
        """
        Realiza o login do usuário, verifica no banco de dados e retorna os dados do usuário.
        :param email: E-mail do usuário.
        :param password: Senha do usuário.
        :return: Dados do usuário, ou dicionário vazio se não encontrado.
        """
        user_data = Database.select_user(email, password)
        if user_data:
            self.user = User(
                user_data["user_id"],
                user_data["user_name"],
                user_data["email"],
                user_data["password"],
                user_data["entry_campaign"],
                user_data["created_campaign"],
                user_data["characters"]
            )
            return user_data
        return {}

    def register(self, user_name: str, email: str, password: str, confirm_password: str) -> bool:
        """
        Realiza o cadastro de um novo usuário.
        :param user_name: Nome do usuário.
        :param email: E-mail do usuário.
        :param password: Senha do usuário.
        :param confirm_password: Confirmação da senha.
        :return: True se o cadastro foi bem-sucedido, False caso contrário.
        """
        if password != confirm_password:
            return False  # Senha não confere
        if len(password) < 6:
            return False  # Senha muito curta

        user_data = {
            "user_name": user_name,
            "email": email,
            "password": password
        }

        user_id = Database.insert_user(user_data)
        if user_id:
            self.user = User(user_id, user_name, email, password, [], [], [])
            return True
        return False

    def get_campaing_data(self, id: list):

        campaings = Database.select_any_campaign(id)
        
        return campaings

    def insert_entry_campaign(self, code: int, character: List[str]) -> bool:
        """
        Insere o usuário em uma campanha, criando personagens associados.
        :param code: Código da campanha.
        :param character: Dados do personagem a ser inserido.
        :return: True se inserção bem-sucedida, False caso contrário.
        """
        try:
            # Adiciona o usuário à campanha
            self.user.insert_entry_campaign(code)
            # Cria o personagem
            character_code = Database.insert_character(character)
            self.user.insert_character(character_code)
            # Atualiza os dados no banco
            Database.update_entry_campaign_user(code, self.user.get_id())
            Database.update_user_characters(character_code)
            return True
        except Exception as e:
            print(f"Erro ao inserir entrada na campanha: {e}")
            return False

    def create_campaign(self, name: str, desc: str, freq: str, img_link: str, user_id: int) -> bool:
        """
        Cria uma nova campanha no banco de dados.
        :param name: Nome da campanha.
        :param desc: Descrição da campanha.
        :param freq: Frequência da campanha.
        :param img_link: Link para imagem da campanha.
        :return: True se a campanha foi criada com sucesso, False caso contrário.
        """
        created_campaign_code = Database.insert_campaign(name, desc, freq, img_link, user_id)
        if created_campaign_code > 0:
            return True
        return False

    def enter_campaign_as_master(self, code: int) -> Dict[str, Any]:
        """
        Entra em uma campanha como mestre, associando o usuário à campanha.
        :param code: Código da campanha.
        :return: Dados da campanha e tipo de usuário (mestre).
        """
        campaign_data = Database.select_campaign(code)
        if campaign_data:
            self.master = Master(self.user.get_name(), campaign_data["campaign_id"])
            return {"campaign": campaign_data, "user_type": "master"}
        return {}

    def enter_campaign_as_player(self, code: int) -> Dict[str, Any]:
        """
        Entra em uma campanha como jogador, associando o usuário à campanha.
        :param code: Código da campanha.
        :return: Dados da campanha e tipo de usuário (jogador).
        """
        campaign_data = Database.select_campaign(code)
        if campaign_data:
            return {"campaign": campaign_data, "user_type": "player"}
        return {}

    def add_artifact_to_campaign(self, campaign_code: int, name: str, desc: str, category: str) -> bool:
        """
        Adiciona um artefato à campanha.
        :param campaign_code: Código da campanha.
        :param name: Nome do artefato.
        :param desc: Descrição do artefato.
        :param category: Categoria do artefato.
        :return: True se artefato foi adicionado com sucesso, False caso contrário.
        """
        artifact_added = Database.insert_artifact(campaign_code, name, desc, category)
        return artifact_added

    def add_item_to_character(self, artifact_code: int, character_code: int) -> bool:
        """
        Adiciona um artefato ao inventário de um personagem.
        :param artifact_code: Código do artefato.
        :param character_code: Código do personagem.
        :return: True se o artefato foi adicionado com sucesso, False caso contrário.
        """
        return Database.insert_artifact_in_inventory(character_code, artifact_code)

    def remove_item_from_character(self, artifact_code: int, character_code: int) -> bool:
        """
        Remove um artefato do inventário de um personagem.
        :param artifact_code: Código do artefato.
        :param character_code: Código do personagem.
        :return: True se o artefato foi removido com sucesso, False caso contrário.
        """
        return Database.delete_inventory(character_code, artifact_code)
