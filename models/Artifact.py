

class Artifact:
    
    def __init__(self, name: str, desc: str, category: str):
        self._name = name
        self._desc = desc
        self._category = category

    def getName(self) -> str:
        return self._name
   
    def getDesc(self) -> str:
        return self._desc
   
    def getCategory(self) -> str:
        return self._category
    
    def setName(self, name: str):
        self._name = name
   
    def setDesc(self, desc: str):
        self._desc = desc
   
    def setCategory(self, category: str):
        self._category = category
    
    def save(self):
        """Salva ou atualiza o artefato no banco de dados."""
        if self.artifact_id:
            return Database.update_artifact(self.artifact_id, self._name, self._desc, self._category)
        else:
            self.artifact_id = Database.insert_artifact(self.campaign_id, self._name, self._desc, self._category)
            return self.artifact_id

    @staticmethod
    def get_by_id(artifact_id: int):
        """Obtém um artefato do banco de dados pelo ID."""
        return Database.select_artifact(artifact_id)

    @staticmethod
    def delete(artifact_id: int):
        """Deleta um artefato do banco de dados."""
        return Database.delete_artifact(artifact_id)