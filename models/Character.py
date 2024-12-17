from .Database import Database

class Character:
    
    def __init__(self):
        self.database = Database()
        self.query = {
            "register": "INSERT INTO `character` (user_id, campaign_id, name, level, class, img_link, race, `money`, `force`, dest, consti, intel, wisdom, charisma, armor, initi, desloc, hp, mana, b_proef, inspiration) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            "select": "SELECT * FROM character WHERE character_id = %s",
            "update": "UPDATE character SET name = %s, class = %s, img_link = %s, race = %s, money = %s, force = %s, dest = %s, consti = %s, intel = %s, wisdom = %s, charisma = %s, armor = %s, init = %s, desloc = %s, hp = %s, bProef = %s, inspiration = %s WHERE character_id = %s",
            "delete": "DELETE FROM character WHERE character_id = %s",
            "select_ids": "SELECT character_id FROM `character` WHERE user_id = %s",
            "select_by_campaign_user": "SELECT * FROM `character` WHERE campaign_id = %s AND user_id = %s"
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
            character_data['pontos_vida'], 
            default_mana, 
            character_data['bonus_proef'], 
            character_data['inspiracao']
        )
        
        if self.database.execute_query(self.query["register"], values):
            return self.database.return_last_insert()
        return 0