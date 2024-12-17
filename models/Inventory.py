from . import Database

class Inventory:
    
    def __init__(self):
        self.database = Database()
        self.query = {
            "register": "INSERT INTO inventory (character_id, artifact_id) VALUES (%s, %s)",
            "select": "SELECT artifact_id FROM inventory WHERE character_id = %s",
            "delete": "DELETE FROM inventory WHERE character_id = %s AND artifact_id = %s",
        }

    def insert_item(self, character_id: int, item_id: int):
        values = (character_id, item_id)
        return self.database.execute_query(self.query["register"], values)
    
    def show_items(self, character_id: int):
        value = (character_id,)
        result = self.database.execute_select_query(self.query["select"], value)
        items = []
        for row in result:
            items.append(row[0])

        artifacts = self.database.execute_select_query("SELECT * FROM artifact WHERE artifact_id IN (%s)", tuple(items))
        response = []

        for row in artifacts:
            response.append({
                "name": row[2],
                "desc": row[3]
            })
        return response
        
