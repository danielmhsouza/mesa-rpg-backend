from typing import List, Dict

class Campaign:
    def __init__(self, code: int, master: int, name: str, desc: str, freq: str, img_link: str):
        self.code = code
        self.master = master
        self.name = name
        self.desc = desc
        self.freq = freq
        self.img_link = img_link
        self.catalog = []

    def add_artifact(self, name: str, desc: str, category: str) -> bool:
        """
        Adiciona um artefato ao catálogo da campanha.
        :param name: Nome do artefato.
        :param desc: Descrição do artefato.
        :param category: Categoria do artefato.
        :return: Retorna True se o artefato foi adicionado com sucesso, False caso contrário.
        """
        artifact = {
            "name": name,
            "desc": desc,
            "category": category
        }
        self.catalog.append(artifact)
        return True

    def list_artifacts(self, category: str) -> List[Dict[str, str]]:
        """
        Lista todos os artefatos da campanha pertencentes a uma categoria específica.
        :param category: Categoria dos artefatos a serem listados.
        :return: Lista de dicionários contendo informações sobre os artefatos da categoria.
        """
        return [artifact for artifact in self.catalog if artifact["category"] == category]
