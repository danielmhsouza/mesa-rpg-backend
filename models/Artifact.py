from models.Database import Database


class Artifact:
    
    def __init__(self):
        self.database = Database()
        self.query = {
            "register": "INSERT INTO artifact (campaign_id, name, desc, category) VALUES (%s, %s, %s, %s)",
            "select": "SELECT artifact_id, name, `desc`, category FROM artifact WHERE campaign_id = %s",
            "update": "UPDATE artifact SET name = %s, desc = %s, category = %s WHERE artifact_id = %s",
            "delete": "DELETE FROM artifact WHERE artifact_id = %s",
        }

    def insert_artifact(self, campaign_id: int, name: str, desc: str, category: int) -> bool:
        values = (campaign_id, name, desc, category)
        return self.database.execute_query(self.query["register"], values)

    def get_artifacts(self, campaign_id: int):
        """
        Chama o Database para buscar os artefatos.
        """
        try:
            params = (campaign_id,)
            result = self.database.execute_query(self.query['select'], params)

            artifacts = [
                {
                    "artifact_id": row[0],
                    "name": row[1],
                    "desc": row[2],
                    "category": row[3]
                }
                for row in result
            ]
            return artifacts
        except Exception as e:
            print(f"Erro no controller: {e}")
            return None