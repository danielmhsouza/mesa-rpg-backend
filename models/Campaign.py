from .Database import Database
from .Character import Character

class Campaign:
   
    def __init__(self):
        self.database = Database()
        self.character = Character()
        self.query = {
            "register": "INSERT INTO campaign (user_id, name, description, freq, img_link) VALUES (%s, %s, %s, %s, %s)",
            "select": "SELECT * FROM campaign WHERE campaign_id = %s",
            "update": "UPDATE campaign SET name = %s, description = %s, freq = %s, img_link = %s WHERE campaign_id = %s",
            "delete": "DELETE FROM campaign WHERE campaign_id = %s",
        }
        self.query_entry_campaign = {
        "register": "INSERT INTO entry_campaign (user_id, campaign_id) VALUES (%s, %s)",
        "select": "SELECT campaign_id FROM entry_campaign WHERE user_id = %s",
        "delete": "DELETE FROM entry_campaign WHERE user_id = %s AND campaign_id = %s",
    }

        self.query_created_campaign = {
            "register": "INSERT INTO created_campaign (user_id, campaign_id) VALUES (%s, %s)",
            "select": "SELECT campaign_id FROM created_campaign WHERE user_id = %s",
            "delete": "DELETE FROM created_campaign WHERE user_id = %s AND campaign_id = %s",
        }
    
    def insert_campaign(self, name: str, desc: str, freq: str, img_link: str, user_id: int) -> int:

        values = (user_id, name, desc, freq, img_link)
        if self.database.execute_query(self.query["register"], values):
            campaing_id = self.database.return_last_insert()
            self.insert_created_campaign(user_id, campaing_id)
            return campaing_id

        return 0
    
    def insert_created_campaign(self, user_id: int, campaign_id: int) -> int:

        values = (user_id, campaign_id)
        if self.database.execute_query(self.query_created_campaign["register"], values):
                return self.database.return_last_insert()
        return 0
    
    def insert_entry_campaign(self, user_id: int, campaign_id: int) -> int:
        
        values = (user_id, campaign_id)
        if self.database.execute_query(self.query_entry_campaign["register"], values):
                return self.database.return_last_insert()
        return 0
    
    def select_campaigns(self, user_id: int):

        # 1. Buscar os IDs das campanhas criadas e que o usuário entrou
        query_created = "SELECT campaign_id FROM created_campaign WHERE user_id = %s;"
        query_entry = "SELECT campaign_id FROM entry_campaign WHERE user_id = %s;"

        created_ids = self.database.execute_select_query(query_created, (user_id,))
        entry_ids = self.database.execute_select_query(query_entry, (user_id,))

        # Combinar os IDs e remover duplicados
        campaign_ids = list(set([row[0] for row in created_ids + entry_ids]))

        if not campaign_ids:
            return []

        # 2. Buscar os dados das campanhas
        query_campaigns = "SELECT * FROM campaign WHERE campaign_id IN (%s);" % ','.join(map(str, campaign_ids))
        result = self.database.execute_select_query(query_campaigns)

        # 3. Transformar os resultados em dicionários
        campaigns = []
        for row in result:
            campaigns.append({
                "campaign_id": row[0],
                "user_id": row[1],
                "name": row[2],
                "description": row[3],
                "freq": row[4],
                "img_link": row[5]
            })
        return campaigns

    def select_campaign(self, id: int) -> dict:
        query = "SELECT * FROM campaign WHERE campaign_id = %s"
        campaign = self.database.execute_select_query(query, (id,))
        user_name = self.database.execute_select_query('SELECT user_name FROM user WHERE user_id = %s', (campaign[0][1],))
        
        return {
                    "campaign_id": campaign[0][0],
                    "user_name": user_name,
                    "name": campaign[0][2],
                    "description": campaign[0][3],
                    "freq": campaign[0][4],
                    "img_link": campaign[0][5]
                }