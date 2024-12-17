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
            return True
        return False

 
    #########

    ###### CAMPAIGN METHODS

    def create_campaign(self, name: str, desc: str, freq: str, img_link: str, user_id: int) -> bool:

        created_campaign_code = self.campaign.insert_campaign(name, desc, freq, img_link, user_id)
        if created_campaign_code > 0:
            return True
        return False
    
    
    def insert_entry_campaign(self, id_camp: int, id_user: int):
        return self.campaign.insert_entry_campaign(id_user, id_camp)
    
    def get_campaigns(self, user_id: int) -> List[Dict[str, Any]]:
        return self.campaign.select_campaigns(user_id)
  
    def get_campaign(self, id: int):
        return self.campaign.select_campaign(id)

    def add_artifact_to_campaign(self, artifact_data: dict) -> bool:
        return self.campaign.master.artifact.insert_artifact(artifact_data["campaign_id"], artifact_data["name"], artifact_data["desc"],
                                             artifact_data["category"])

    def get_artifacts(self, campaign_id: int):
        return self.campaign.master.artifact.get_artifacts(campaign_id)
    
        ###### CHARACTER METHODS

    def create_character(self, character: dict, id_camp: int, id_user: int) -> int:
        return self.campaign.character.insert_character(character, id_camp, id_user)
    

    def get_characters_by_campaign_and_user(self, campaign_id: int, user_id: int):
        return self.campaign.character.select_character_by_campaign_and_user(campaign_id, user_id)
    
    def get_all_character_by_campaign(self, campaign_id):
        return self.campaign.character.select_characters_by_campaign(campaign_id)
        #########

    #########
