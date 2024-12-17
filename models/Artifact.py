from models.Database import Database


class Artifact:
    
    def __init__(self):
        self.database = Database()
        self.query = {
            "register": "INSERT INTO artifact (campaign_id, name, desc, category) VALUES (%s, %s, %s, %s)",
            "select": "SELECT * FROM artifact WHERE campaign_id = %s",
            "update": "UPDATE artifact SET name = %s, desc = %s, category = %s WHERE artifact_id = %s",
            "delete": "DELETE FROM artifact WHERE artifact_id = %s",
        }

    def insert_artifact(self, campaign_id: int, name: str, desc: str, category: int) -> bool:
        values = (campaign_id, name, desc, category)
        return self.database.execute_query(self.query["register"], values)

