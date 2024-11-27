from typing import List, Dict

class Campaign:
    def __init__(self, code: int = None, master: int = None, name: str = "", desc: str = "", freq: str = "", img_link: str = ""):
        self.code = code
        self.master = master
        self.name = name
        self.desc = desc
        self.freq = freq
        self.img_link = img_link

    def save(self):
        """Salva ou atualiza a campanha no banco de dados."""
        if self.code:
            return Database.update_campaign(self.code, self.name, self.desc, self.freq, self.img_link)
        else:
            self.code = Database.insert_campaign(self.name, self.desc, self.freq, self.img_link, self.master)
            return self.code

    @staticmethod
    def get_by_id(campaign_id: int):
        """Obtém uma campanha do banco de dados dado o ID."""
        return Database.select_campaign(campaign_id)

    @staticmethod
    def delete(campaign_id: int):
        """Deleta uma campanha e seus dados relacionados (entradas e personagens)."""
        return Database.delete_campaign(campaign_id)

    def add_artifact(self, name: str, desc: str, category: str) -> bool:
        """
        Adiciona um novo artefato à campanha.
        :param name: Nome do artefato.
        :param desc: Descrição do artefato.
        :param category: Categoria do artefato.
        :return: Retorna True se o artefato foi adicionado com sucesso, False caso contrário.
        """
        return Database.insert_artifact(self.code, name, desc, category)

    @staticmethod
    def list_artifacts(campaign_id: int, category: str) -> List[Dict[str, str]]:
        """
        Lista todos os artefatos de uma campanha pertencentes a uma categoria específica.
        :param campaign_id: ID da campanha.
        :param category: Categoria dos artefatos a serem listados.
        :return: Lista de dicionários contendo informações sobre os artefatos da categoria.
        """
        artifacts = Database.select_campaign_artifacts(campaign_id)
        return [artifact for artifact in artifacts if artifact["category"] == category]
