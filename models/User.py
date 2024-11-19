class User:
    def __init__(self, id: int, name: str, email: str, password: str, entry_campaign: list, created_campaign: list, characters: list):
        self._id = id
        self._name = name
        self._email = email
        self._password = password
        self._entry_campaign = entry_campaign
        self._created_campaign = created_campaign
        self._characters = characters

    def insert_entry_campaign(self, code: str):
        """Adiciona uma campanha à lista de campanhas de entrada do usuário."""
        if code not in self._entry_campaign:
            self._entry_campaign.append(code)
            Database.update_user_campaign(self._id, self._entry_campaign)  # Atualiza o banco de dados

    def insert_character(self, character_code: str):
        """Adiciona um personagem ao usuário."""
        if character_code not in self._characters:
            self._characters.append(character_code)
            Database.update_user_characters(self._id, self._characters)  # Atualiza o banco de dados

    def insert_created_campaign(self, created_campaign_code: str):
        """Adiciona uma campanha criada à lista de campanhas do usuário."""
        if created_campaign_code not in self._created_campaign:
            self._created_campaign.append(created_campaign_code)
            Database.update_user_created_campaign(self._id, self._created_campaign)  # Atualiza o banco de dados

    def get_name(self) -> str:
        """Retorna o nome do usuário."""
        return self._name

    def get_id(self) -> int:
        """Retorna o ID do usuário."""
        return self._id

    def remove_my_campaign(self, code: str) -> bool:
        """Remove uma campanha criada do usuário."""
        if code in self._created_campaign:
            self._created_campaign.remove(code)
            Database.update_user_created_campaign(self._id, self._created_campaign)  # Atualiza o banco de dados
            return True
        return False

    def remove_entry_campaign(self, code: str) -> bool:
        """Remove uma campanha de entrada do usuário."""
        if code in self._entry_campaign:
            self._entry_campaign.remove(code)
            Database.update_user_campaign(self._id, self._entry_campaign)  # Atualiza o banco de dados
            return True
        return False

    def edit_password(self, old_password: str, new_password: str) -> bool:
        """Altera a senha do usuário."""
        if old_password == self._password:
            self._password = new_password
            Database.update_user_password(self._id, new_password)  # Atualiza o banco de dados
            return True
        return False

    def edit_name(self, new_name: str):
        """Altera o nome do usuário."""
        self._name = new_name
        Database.update_user_name(self._id, new_name)  # Atualiza o banco de dados
