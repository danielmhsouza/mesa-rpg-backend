from typing import List, Dict, Any
import mariadb
import Database.querys as db
import os
from dotenv import load_dotenv

class Database:
    _instance = None  # Atributo de classe para armazenar a única instância

    def __new__(cls, *args, **kwargs):
        """Garante que apenas uma instância da classe seja criada."""
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._initialized = False  # Flag para inicialização
        return cls._instance

    def __init__(self):
        """Evita reinicializar a instância existente."""
        if self._initialized:
            return
        
        load_dotenv()  # Carrega as variáveis do arquivo .env
        self._hostname: str = os.getenv("DB_HOST")  
        self._user: str = os.getenv("DB_USER")  
        self._password: str = os.getenv("DB_PASSWORD")  
        self._db_name: str = os.getenv("DB_NAME")  
        self._port: int = int(os.getenv("DB_PORT", 3306))
        self._connect()
        self._initialized = True

    def _connect(self):
        """Estabelece uma conexão com o banco de dados."""
        try:
            self.db = mariadb.connect(
                host=self._hostname,
                port=3306,
                user=self._user,
                password=self._password,
                database=self._db_name
            )
            print("Conexão bem-sucedida com o banco MariaDB!")
        except mariadb.Error as e:
            print(f"Erro ao conectar ao MariaDB: {e}")
            self.db = None

    def _check_connection(self):
        """Verifica se a conexão ainda está ativa, reconectando se necessário."""
        try:
            self.db.ping()  # Verifica se a conexão está ativa
        except mariadb.Error:
            print("Conexão perdida. Reconectando...")
            self._connect()

    def execute_query(self, query: str, values: tuple = None) -> bool:
        self._check_connection()
        try:
            mycursor = self.db.cursor()
            if values:
                mycursor.execute(query, values)
            else:
                mycursor.execute(query)
            self.db.commit()
            return True
        except mariadb.Error as e:
            print(f"Erro ao executar query: {e}")
            return False
        finally:
            mycursor.close()

    def execute_select_query(self, query: str, values: tuple = None) -> list:
        self._check_connection()
        try:
            mycursor = self.db.cursor()
            if values:
                mycursor.execute(query, values)
            else:
                mycursor.execute(query)
            return mycursor.fetchall()
        except mariadb.Error as e:
            print(f"Erro ao executar SELECT query: {e}")
            return []
        finally:
            mycursor.close()

    def return_last_insert(self):
        try:
            mycursor = self.db.cursor()
            mycursor.execute("SELECT LAST_INSERT_ID()")
            id = mycursor.fetchone()[0]
            return id
        finally:
            mycursor.close()
    
    def delete_campaign(self, campaign_id: int) -> bool:
        """
        Deleta uma campanha do banco de dados.
        :param campaign_id: ID da campanha a ser deletada.
        :return: Retorna True se a exclusão for bem-sucedida, False caso contrário.
        """
        try:
            # Excluir as entradas de campanha associadas à campanha
            query_entry_campaign = "DELETE FROM entry_campaign WHERE campaign_id = %s"
            values_entry_campaign = (campaign_id,)
            self._execute_query(query_entry_campaign, values_entry_campaign)

            # Excluir personagens relacionados à campanha (se necessário)
            query_characters = "DELETE FROM character WHERE campaign_id = %s"
            values_characters = (campaign_id,)
            self._execute_query(query_characters, values_characters)

            # Excluir a campanha
            query = db.query_campaigns["delete"]
            values = (campaign_id,)
            return self._execute_query(query, values)
        except Exception as e:
            print(f"Erro ao excluir campanha: {e}")
            return False

    def select_character(self, character_id: int) -> Dict[str, Any]:
        """
        Seleciona um personagem do banco de dados com base no ID do personagem.
        :param character_id: ID do personagem a ser selecionado.
        :return: Dicionário contendo as informações do personagem (ID, nome, classe, atributos, etc.).
        """
        query = db.query_characters["select"]
        values = (character_id,)
        result = self._execute_select_query(query, values)

        if result:
            return {
                "character_id": result[0][0],
                "user_id": result[0][1],
                "campaign_id": result[0][2],
                "name": result[0][3],
                "level": result[0][4],
                "class": result[0][5],
                "img_link": result[0][6],
                "race": result[0][7],
                "money": result[0][8],
                "force": result[0][9],
                "dest": result[0][10],
                "consti": result[0][11],
                "intel": result[0][12],
                "wisdom": result[0][13],
                "charisma": result[0][14],
                "armor": result[0][15],
                "initi": result[0][16],
                "desloc": result[0][17],
                "hp": result[0][18],
                "mana": result[0][19],
                "b_proef": result[0][20],
                "inspiration": result[0][21]
            }
        return {}

    

    def update_character(self, character_data: Dict[str, Any]) -> bool:
        """
        Atualiza as informações de um personagem no banco de dados.
        :param character_data: Dicionário contendo as novas informações do personagem (nome, classe, raça, atributos, etc.).
        :return: Retorna True se a atualização for bem-sucedida, False caso contrário.
        """
        query = db.query_characters["update"]
        values = (
            character_data['name'], character_data['class'], character_data['img_link'], character_data['race'],
            character_data['money'], character_data['force'], character_data['dest'], character_data['consti'],
            character_data['intel'], character_data['wisdom'], character_data['charisma'], character_data['armor'],
            character_data['initi'], character_data['desloc'], character_data['hp'], character_data['mana'],
            character_data['b_proef'], character_data['inspiration'], character_data['character_id']
        )
        return self._execute_query(query, values)

    def delete_character(self, character_id: int) -> bool:
        """
        Deleta um personagem do banco de dados com base no ID do personagem.
        :param character_id: ID do personagem a ser deletado.
        :return: Retorna True se a exclusão for bem-sucedida, False caso contrário.
        """
        query = db.query_characters["delete"]
        values = (character_id,)
        return self._execute_query(query, values)
    
    def update_entry_campaign_user(self, code: int, user_id: int) -> bool:
        """
        Atualiza a entrada de campanha do usuário no banco de dados.
        :param code: Código da campanha a ser atualizada.
        :param user_id: ID do usuário que entra ou altera sua campanha.
        :return: Retorna True se a atualização for bem-sucedida, False caso contrário.
        """
        query = db.query_entry_campaign["register"]
        values = (user_id, code)
        return self._execute_query(query, values)

    def insert_artifact_in_inventory(self, character_id: int, artifact_id: int) -> bool:
        """
        Adiciona um artefato ao inventário de um personagem.
        :param character_id: ID do personagem.
        :param artifact_id: ID do artefato a ser adicionado.
        :return: Retorna True se o artefato foi adicionado com sucesso, False caso contrário.
        """
        query = db.query_inventory["register"]
        values = (character_id, artifact_id)
        return self._execute_query(query, values)
    
    def select_inventory(self, character_id: int) -> List[Dict[str, Any]]:
        """Retorna todos os artefatos de um personagem do banco de dados."""
        query = db.query_inventory["select"]
        values = (character_id,)
        result = self._execute_select_query(query, values)
        artifacts = []
        for row in result:
            artifacts.append(Artifact.get_by_id(row[1]))  # Cria objetos Artifact
        return artifacts

    def delete_inventory(self, character_id: int, artifact_id: int) -> bool:
        """
        Remove um artefato do inventário de um personagem.
        :param character_id: ID do personagem.
        :param artifact_id: ID do artefato a ser removido.
        :return: Retorna True se o artefato foi removido com sucesso, False caso contrário.
        """
        query = db.query_inventory["delete"]
        values = (character_id, artifact_id)
        return self._execute_query(query, values)

    #Funções de Artefato
    def insert_artifact(self, campaign_id: int, name: str, desc: str, category: str) -> bool:
        """Insere um artefato na campanha no banco de dados."""
        query = db.query_artifacts["register"]
        values = (campaign_id, name, desc, category)
        return self._execute_query(query, values)

    def select_artifact(self, artifact_id: int) -> Dict[str, Any]:
        """
        Seleciona um artefato do banco de dados com base no ID do artefato.
        :param artifact_id: ID do artefato a ser selecionado.
        :return: Dicionário contendo as informações do artefato (ID, nome, descrição, categoria).
        """
        query = db.query_artifacts["select"]
        values = (artifact_id,)
        result = self._execute_select_query(query, values)
        if result:
            return {
                "artifact_id": result[0][0],
                "campaign_id": result[0][1],
                "name": result[0][2],
                "desc": result[0][3],
                "category": result[0][4]
            }
        return {}

    def update_artifact(self, artifact_id: int, name: str, desc: str, category: str) -> bool:
        """
        Atualiza as informações de um artefato no banco de dados.
        :param artifact_id: ID do artefato a ser atualizado.
        :param name: Novo nome do artefato.
        :param desc: Nova descrição do artefato.
        :param category: Nova categoria do artefato.
        :return: Retorna True se a atualização for bem-sucedida, False caso contrário.
        """
        query = db.query_artifacts["update"]
        values = (name, desc, category, artifact_id)
        return self._execute_query(query, values)


    def delete_artifact(self, artifact_id: int) -> bool:
        """Remove um artefato do banco de dados."""
        query = db.query_artifacts["delete"]
        values = (artifact_id,)
        return self._execute_query(query, values)