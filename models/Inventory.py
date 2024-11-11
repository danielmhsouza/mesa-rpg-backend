

class Inventory:
    def __init__(self):
        self.artifacts = []

    def add_artifact(self, artifact, index: int) -> bool:
        """
        Adiciona um artefato ao inventário na posição especificada pelo índice.
        :param artifact: O artefato a ser adicionado.
        :param index: O índice onde o artefato será adicionado.
        :return: Retorna True se o artefato foi adicionado com sucesso, False caso contrário.
        """
        if 0 <= index <= len(self.artifacts):
            self.artifacts.insert(index, artifact)
            return True
        return False

    def drop_artifact(self, index: int) -> bool:
        """
        Remove um artefato do inventário na posição especificada pelo índice.
        :param index: O índice do artefato a ser removido.
        :return: Retorna True se o artefato foi removido com sucesso, False caso contrário.
        """
        if 0 <= index < len(self.artifacts):
            self.artifacts.pop(index)
            return True
        return False
