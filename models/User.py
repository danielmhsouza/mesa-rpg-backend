

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
        if code not in self._entry_campaign:
            self._entry_campaign.append(code)

    def insert_character(self, character_code: str):
        if character_code not in self._characters:
            self._characters.append(character_code)

    def insert_created_campaign(self, created_campaign_code: str):
        if created_campaign_code not in self._created_campaign:
            self._created_campaign.append(created_campaign_code)

    def get_name(self) -> str:
        return self._name

    def get_id(self) -> int:
        return self._id

    def remove_my_campaign(self, code: str) -> bool:
        if code in self._created_campaign:
            self._created_campaign.remove(code)
            return True
        return False

    def remove_entry_campaign(self, code: str) -> bool:
        if code in self._entry_campaign:
            self._entry_campaign.remove(code)
            return True
        return False

    def edit_password(self, old_password: str, new_password: str) -> bool:
        if old_password == self._password:
            self._password = new_password
            return True
        return False

    def edit_name(self, new_name: str):
        self._name = new_name
