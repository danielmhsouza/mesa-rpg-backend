from typing import List, Dict, Any

from models.User import User
from models.Campaign import Campaign
from models.Master import Master
from models.Database import Database

class Controller:
    def __init__(self):
        self.user = None
        self.campaign = None
        self.master = None

    def login(self, email: str, password: str) -> Dict[str, Any]:
        user_data = Database.select_user(email, password)
        self.user = User(
            user_data["id"],
            user_data["name"],
            user_data["email"],
            user_data["password"],
            user_data["entry_campaign"],
            user_data["created_campaign"],
            user_data["characters"]
        )
        return user_data

    def insert_entry_campaign(self, code: int, character: List[str]) -> bool:
        try:
            self.user.insert_entry_campaign(code)
            character_code = Database.insert_character(character)
            self.user.insert_character(character_code)
            Database.update_entry_campaign_user(code)
            Database.update_user_characters(character_code)
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def create_campaign(self, name: str, desc: str, freq: str, img_link: str) -> bool:
        created_campaign_code = Database.create_campaign(name, desc, freq, img_link, self.user.get_id())
        if created_campaign_code > 0:
            self.user.insert_created_campaign(created_campaign_code)
            return True
        return False

    def enter_campaign_as_master(self, code: int, id_user: int) -> Dict[str, Any]:
        campaign_data = Database.select_campaign_data(code)
        self.master = Master(self.user.get_name(), campaign_data["id"])
        return {"campaign": campaign_data, "user_type": "master"}

    def enter_campaign_as_player(self, code: int, id_user: int) -> Dict[str, Any]:
        campaign_data = Database.select_campaign_data(code)
        return {"campaign": campaign_data, "user_type": "player"}

class SpellBoundTable:
    users = []
    campaigns = []
    artifacts = []
    players = []

    @classmethod
    def login(cls, email, password):
        for user in cls.users:
            if user['email'] == email and user['password'] == password:
                return "Entrar na Plataforma"
            elif user['email'] == email:
                return "Email ou senha inválido"
        return "Usuário não cadastrado"

    @classmethod
    def register(cls, name, email, password, confirm_password):
        if not name or not email or not password or not confirm_password:
            return "Campos obrigatórios"
        if password != confirm_password:
            return "Confirme a senha corretamente"
        if len(password) < 6:
            return "Digite uma senha válida (pelo menos 6 caract...)"
        for user in cls.users:
            if user['email'] == email:
                return "Email já cadastrado"
        cls.users.append({"name": name, "email": email, "password": password})
        return "Cadastro realizado"

    @classmethod
    def create_campaign(cls, name, description, image_link, frequency):
        if not name or not description or not frequency:
            return "Preencher campos obrigatórios"
        if not cls.is_valid_image_link(image_link):
            return "Link inválido ou ignorar link"
        cls.campaigns.append({"name": name, "description": description, "image_link": image_link, "frequency": frequency})
        return "Campanha Criada"

    @staticmethod
    def is_valid_image_link(link):
        return link.startswith("http") and (".jpg" in link or ".png" in link)

    @classmethod
    def join_campaign(cls, campaign_name, character_created):
        if not character_created:
            return "Não entrará na campanha"
        return "Campanha aparece na página inicial"

    @classmethod
    def add_artifact(cls, player, artifact):
        if artifact not in cls.artifacts:
            return "Artefato inexistente"
        if player not in cls.players:
            return "Jogador fora da campanha"
        return f"{player} tem acesso ao artefato"

    @classmethod
    def remove_artifact(cls, player, artifact):
        if artifact not in cls.artifacts:
            return "Artefato inexistente"
        if player not in cls.players:
            return "Jogador fora da campanha"
        return f"{artifact} removido do inventário do {player}"