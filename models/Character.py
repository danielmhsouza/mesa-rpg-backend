from .Database import Database
from .Inventory import Inventory
class Character:
    
    def __init__(self):
        self.database = Database()
        self.inventory = Inventory()
        self.query = {
            "register": "INSERT INTO `character` (user_id, campaign_id, name, level, class, img_link, race, `money`, `force`, dest, consti, intel, wisdom, charisma, armor, initi, desloc, hp, mana, b_proef, inspiration) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            "select": "SELECT * FROM character WHERE character_id = %s",
            "update": "UPDATE character SET name = %s, class = %s, img_link = %s, race = %s, money = %s, force = %s, dest = %s, consti = %s, intel = %s, wisdom = %s, charisma = %s, armor = %s, init = %s, desloc = %s, hp = %s, bProef = %s, inspiration = %s WHERE character_id = %s",
            "delete": "DELETE FROM character WHERE character_id = %s",
            "select_ids": "SELECT character_id FROM `character` WHERE user_id = %s",
            "select_by_campaign_user": "SELECT * FROM `character` WHERE campaign_id = %s AND user_id = %s",
            "select_all_by_campaign": "SELECT * FROM `character` WHERE campaign_id = %s"
        }

    def insert_character(self, character_data: dict, camp_id: int, user_id: int) -> int:

        default_money = 150
        default_mana = 200
        default_level = 1
        
        values = (
            user_id, 
            camp_id, 
            character_data['name'],
            default_level,
            character_data['classe'],
            character_data['img_link'], 
            character_data['race'], 
            default_money, 
            character_data['force'],
            character_data['destreza'], 
            character_data['constituicao'], 
            character_data['inteligencia'], 
            character_data['sabedoria'],
            character_data['carisma'], 
            character_data['armadura'], 
            character_data['iniciativa'], 
            character_data['deslocamento'],
            int(character_data['pontos_vida'])+100, 
            default_mana, 
            character_data['bonus_proef'], 
            character_data['inspiracao']
        )
        
        if self.database.execute_query(self.query["register"], values):
            return self.database.return_last_insert()
        return 0
    
    def select_character_by_campaign_and_user(self, campaign_id: int, user_id: int) -> list:

        values = (campaign_id, user_id)
        result = self.database.execute_select_query(self.query["select_by_campaign_user"], values)

        characters = []
        for row in result:
            characters.append({
                "character_id": row[0],
                "user_id": row[1],
                "campaign_id": row[2],
                "name": row[3],
                "level": row[4],
                "class": row[5],
                "img_link": row[6],
                "race": row[7],
                "money": row[8],
                "force": row[9],
                "dest": row[10],
                "consti": row[11],
                "intel": row[12],
                "wisdom": row[13],
                "charisma": row[14],
                "armor": row[15],
                "initi": row[16],
                "desloc": row[17],
                "hp": row[18],
                "mana": row[19],
                "b_proef": row[20],
                "inspiration": row[21]
            })
        return characters
    
    def select_characters_by_campaign(self, campaign_id):
        values = (campaign_id,)
        result = self.database.execute_select_query(self.query["select_all_by_campaign"], values)

        characters = []
        for row in result:
            characters.append({
                "character_id": row[0],
                "user_id": row[1],
                "campaign_id": row[2],
                "name": row[3],
                "level": row[4],
                "class": row[5],
                "img_link": row[6],
                "race": row[7],
                "money": row[8],
                "force": row[9],
                "dest": row[10],
                "consti": row[11],
                "intel": row[12],
                "wisdom": row[13],
                "charisma": row[14],
                "armor": row[15],
                "initi": row[16],
                "desloc": row[17],
                "hp": row[18],
                "mana": row[19],
                "b_proef": row[20],
                "inspiration": row[21]
            })
        return characters