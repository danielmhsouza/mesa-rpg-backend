

class Master:
    def __init__(self, name: str, campaign_code: int):
        self.name = name
        self.campaign_code = campaign_code

    def add_artifact(self, name: str, desc: str, category: str) -> bool:
        # Implementar a lógica para adicionar um artefato
         return Database.insert_artifact(self.campaign_code, name, desc, category)

    def remove_artifact(self, index: int):
        # Implementar a lógica para remover um artefato pelo índice
        return Database.delete_artifact(artifact_id)

    def add_item_to_character(self, artifact_index: int, character_index: int) -> bool:
        # Implementar a lógica para adicionar um item ao personagem
        return Database.insert_inventory(character_id, artifact_id)
