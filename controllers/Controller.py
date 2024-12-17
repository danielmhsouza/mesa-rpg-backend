from typing import List, Dict, Any
from models.User import User
from models.Campaign import Campaign
from models.Master import Master
from models.Artifact import Artifact
from models.Database import Database

class Controller:
    def __init__(self):
        self.user = User()
        self.campaign = Campaign()
        self.master = None
        self.database = Database()

    ###### USER METHODS
    
    def login(self, email: str, password: str) -> Dict[str, Any]:
        """
        Realiza o login do usuário, verifica no banco de dados e retorna os dados do usuário.
        :param email: E-mail do usuário.
        :param password: Senha do usuário.
        :return: Dados do usuário, ou dicionário vazio se não encontrado.
        """
        user_data = self.user.select_user(email, password)
        if user_data:
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

        user_id = self.user.insert_user(user_data)
        print(f"\n\n Database response: {user_id} \n\n")
        if user_id:
            self.user = User(user_id, user_name, email, password, [], [], [])
            return True
        return False

 
    #########

    ###### CAMPAIGN METHODS

    def create_campaign(self, name: str, desc: str, freq: str, img_link: str, user_id: int) -> bool:

        created_campaign_code = self.campaign.insert_campaign(name, desc, freq, img_link, user_id)
        if created_campaign_code > 0:
            return True
        return False
    
    def create_character(self, character: dict, id_camp: int, id_user: int) -> int:
        return self.campaign.character.insert_character(character, id_camp, id_user)
    
    def insert_entry_campaign(self, id_camp: int, id_user: int):
        return self.campaign.insert_entry_campaign(id_user, id_camp)
    
    def get_campaigns(self, user_id: int) -> List[Dict[str, Any]]:
        return self.campaign.select_campaigns(user_id)
  
    def get_campaign(self, id: int):
        return self.campaign.select_campaign(id)
    
    
    #########

    def get_characters_by_campaign_and_user(self, campaign_id: int, user_id: int):
        return self.database.select_character_by_campaign_and_user(campaign_id, user_id)

    def delete_character(self, id: int):
        self.database.delete_character(id)
        
    def enter_campaign_as_master(self, code: int) -> Dict[str, Any]:
        """
        Entra em uma campanha como mestre, associando o usuário à campanha.
        :param code: Código da campanha.
        :return: Dados da campanha e tipo de usuário (mestre).
        """
        campaign_data = self.database.select_campaign(code)
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
        campaign_data = self.database.select_campaign(code)
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
        artifact_added = self.database.insert_artifact(campaign_code, name, desc, category)
        return artifact_added

    def add_item_to_character(self, artifact_code: int, character_code: int) -> bool:
        """
        Adiciona um artefato ao inventário de um personagem.
        :param artifact_code: Código do artefato.
        :param character_code: Código do personagem.
        :return: True se o artefato foi adicionado com sucesso, False caso contrário.
        """
        return self.database.insert_artifact_in_inventory(character_code, artifact_code)

    def remove_item_from_character(self, artifact_code: int, character_code: int) -> bool:
        """
        Remove um artefato do inventário de um personagem.
        :param artifact_code: Código do artefato.
        :param character_code: Código do personagem.
        :return: True se o artefato foi removido com sucesso, False caso contrário.
        """
        return self.database.delete_inventory(character_code, artifact_code)
