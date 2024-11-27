class Inventory:
    def __init__(self, character_id: int):
        self.character_id = character_id
        self.artifacts = self.load_artifacts_from_db()

    def load_artifacts_from_db(self):
        """Carrega todos os artefatos associados a este personagem do banco de dados."""
        return Database.select_inventory(self.character_id)

    def add_artifact(self, artifact, index: int) -> bool:
        """
        Adiciona um artefato ao inventário na posição especificada pelo índice.
        :param artifact: O artefato a ser adicionado.
        :param index: O índice onde o artefato será adicionado.
        :return: Retorna True se o artefato foi adicionado com sucesso, False caso contrário.
        """
        if 0 <= index <= len(self.artifacts):
            self.artifacts.insert(index, artifact)
            if Database.insert_inventory(self.character_id, artifact.artifact_id):
                return True
            else:
                self.artifacts.remove(artifact)
        return False

    def drop_artifact(self, index: int) -> bool:
        """
        Remove um artefato do inventário na posição especificada pelo índice.
        :param index: O índice do artefato a ser removido.
        :return: Retorna True se o artefato foi removido com sucesso, False caso contrário.
        """
        if 0 <= index < len(self.artifacts):
            artifact = self.artifacts.pop(index)
            if Database.delete_inventory(self.character_id, artifact.artifact_id):
                return True
            else:
                self.artifacts.insert(index, artifact)
        return False
