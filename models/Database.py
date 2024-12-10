from typing import List, Dict, Any
import mariadb
import Database.querys as db

class Database:
    def __init__(self):
        self._hostname: str = 'mysql.freehostia.com'
        self._password: str = 'Ssswww#123'
        self._db_name: str = 'dansou481_spellboundtable'
        self._user: str = "dansou481_spellboundtable"

        try:
            # Estabelecendo a conexão
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

    def _execute_query(self, query: str, values:tuple=None) -> bool:
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
    
    def _execute_select_query(self, query: str, values: tuple=None) -> list:
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


    def insert_user(self, user_data: Dict[str, Any]) -> int:
        """
        Insere um novo usuário no banco de dados e retorna o ID do usuário inserido.
        :param user_data: Dicionário contendo as informações do usuário, incluindo nome, e-mail e senha.
        :return: O ID do usuário inserido no banco de dados.
        """
        query = db.query_users["register"]
        values = (user_data['user_name'], user_data['email'], user_data['password'])
        if self._execute_query(query, values):
            try:
                mycursor = self.db.cursor()
                mycursor.execute("SELECT LAST_INSERT_ID()")
                return mycursor.fetchone()[0]
            finally:
                mycursor.close()
        return 0

    def select_user(self, email: str, password: str) -> Dict[str, Any]:
        """
        Seleciona um usuário do banco de dados com base no e-mail e senha fornecidos.
        :param email: E-mail do usuário.
        :param password: Senha do usuário.
        :return: Dicionário contendo informações do usuário (ID, nome, e-mail e senha), ou um dicionário vazio se não encontrar o usuário.
        """
        query = db.query_users["select"]
        values = (email, password)
        result = self._execute_select_query(query, values)
        if result:
  
            return {
                "user_id": result[0][0],
                "user_name": result[0][1],
                "email": result[0][2],
                "password": result[0][3],

            }
        return {}

    def update_user(self, user_data: Dict[str, Any]) -> bool:
        """
        Atualiza as informações de um usuário no banco de dados.
        :param user_data: Dicionário contendo as novas informações do usuário (nome, e-mail, senha e ID).
        :return: Retorna True se a atualização for bem-sucedida, False caso contrário.
        """
        query = db.query_users["update"]
        values = (user_data['user_name'], user_data['email'], user_data['password'], user_data['user_id'])
        return self._execute_query(query, values)


    def update_user_password(self, user_id: int, new_password: str) -> bool:
        """Atualiza a senha de um usuário."""
        query = "UPDATE user SET password = %s WHERE user_id = %s"
        values = (new_password, user_id)
        return self._execute_query(query, values)


    def update_user_name(self, user_id: int, new_name: str) -> bool:
        """Atualiza o nome de um usuário."""
        query = "UPDATE user SET user_name = %s WHERE user_id = %s"
        values = (new_name, user_id)
        return self._execute_query(query, values)

    
    def update_user_campaign(self, user_id: int, entry_campaign: list) -> bool:
        """Atualiza a lista de campanhas de entrada de um usuário."""
        query = "UPDATE user SET entry_campaign = %s WHERE user_id = %s"
        values = (entry_campaign, user_id)
        return self._execute_query(query, values)


    def update_user_characters(self, user_id: int, characters: list) -> bool:
        """Atualiza a lista de personagens de um usuário."""
        query = "UPDATE user SET characters = %s WHERE user_id = %s"
        values = (characters, user_id)
        return self._execute_query(query, values)

    def update_user_created_campaign(self, user_id: int, created_campaign: list) -> bool:
        """Atualiza a lista de campanhas criadas de um usuário."""
        query = "UPDATE user SET created_campaign = %s WHERE user_id = %s"
        values = (created_campaign, user_id)
        return self._execute_query(query, values)

  
    def insert_campaign(self, name: str, desc: str, freq: str, img_link: str, user_id: int) -> int:
        """
        Insere uma nova campanha no banco de dados e retorna o ID da campanha inserida.
        :param name: Nome da campanha.
        :param desc: Descrição da campanha.
        :param freq: Frequência da campanha.
        :param img_link: Link da imagem da campanha.
        :param user_id: ID do usuário que cria a campanha.
        :return: O ID da campanha inserida no banco de dados.
        """
        query = db.query_campaigns["register"]
        values = (user_id, name, desc, freq, img_link)
        if self._execute_query(query, values):
            try:
                mycursor = self.db.cursor()
                mycursor.execute("SELECT LAST_INSERT_ID()")
                campaing_id = mycursor.fetchone()[0]
                self.insert_created_campaign(user_id, campaing_id)
                return campaing_id
            finally:
                mycursor.close()
        return 0
    
    def insert_created_campaign(self, user_id: int, campaign_id: int) -> int:

        query = db.query_created_campaign["register"]
        values = (user_id, campaign_id)
        if self._execute_query(query, values):
            try:
                mycursor = self.db.cursor()
                mycursor.execute("SELECT LAST_INSERT_ID()")
                return mycursor.fetchone()[0]
            finally:
                mycursor.close()
        return 0

    def select_campaigns(self, user_id: int) -> List[Dict[str, Any]]:
        """
        Busca todas as campanhas associadas ao usuário (criadas ou que ele entrou).
        :param user_id: ID do usuário.
        :return: Lista com as campanhas associadas.
        """
        # 1. Buscar os IDs das campanhas criadas e que o usuário entrou
        query_created = "SELECT campaign_id FROM created_campaign WHERE user_id = %s;"
        query_entry = "SELECT campaign_id FROM entry_campaign WHERE user_id = %s;"

        created_ids = self._execute_select_query(query_created, (user_id,))
        entry_ids = self._execute_select_query(query_entry, (user_id,))

        # Combinar os IDs e remover duplicados
        campaign_ids = list(set([row[0] for row in created_ids + entry_ids]))

        if not campaign_ids:
            return []  # Se não houver campanhas, retorna lista vazia

        # 2. Buscar os dados das campanhas
        query_campaigns = "SELECT * FROM campaign WHERE campaign_id IN (%s);" % ','.join(map(str, campaign_ids))
        result = self._execute_select_query(query_campaigns)

        # 3. Transformar os resultados em dicionários
        campaigns = []
        for row in result:
            campaigns.append({
                "campaign_id": row[0],
                "user_id": row[1],
                "name": row[2],
                "description": row[3],
                "freq": row[4],
                "img_link": row[5]
            })
        return campaigns

    # @staticmethod
    # def select_any_campaign(campaign_ids: list) -> Dict[str, Any]:
    #     """
    #     Seleciona uma campanha do banco de dados com base no ID da campanha.
    #     :param campaign_id: ID da campanha a ser selecionada.
    #     :return: Dicionário contendo as informações da campanha (ID, nome, descrição, frequência e link da imagem), ou um dicionário vazio se não encontrar a campanha.
    #     """
    #     query = "SELECT * FROM campaign WHERE campaign_id IN (%s)" % ','.join(map(str, campaign_ids))
    #     result = self._execute_select_query(query)
    #     if result:
    #         return {
    #             "campaign_id": result[0][0],
    #             "user_id": result[0][1],
    #             "name": result[0][2],
    #             "description": result[0][3],
    #             "freq": result[0][4],
    #             "img_link": result[0][5]
    #         }
    #     return {}

    def update_campaign(self, campaign_data: Dict[str, Any]) -> bool:
        """
        Atualiza as informações de uma campanha no banco de dados.
        :param campaign_data: Dicionário contendo as novas informações da campanha (nome, descrição, frequência, link da imagem e ID).
        :return: Retorna True se a atualização for bem-sucedida, False caso contrário.
        """
        query = db.query_campaigns["update"]
        values = (campaign_data['name'], campaign_data['description'], campaign_data['freq'], campaign_data['img_link'], campaign_data['campaign_id'])
        return self._execute_query(query, values)
    
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


    def insert_character(self, character_data: Dict[str, Any]) -> int:
        """
        Insere um novo personagem no banco de dados e retorna o ID do personagem inserido.
        :param character_data: Dicionário contendo as informações do personagem (nome, classe, raça, atributos, etc.).
        :return: O ID do personagem inserido no banco de dados.
        """
        query = db.query_characters["register"]
        values = (
            character_data['user_id'], character_data['campaign_id'], character_data['name'], character_data['class'],
            character_data['img_link'], character_data['race'], character_data['money'], character_data['force'],
            character_data['dest'], character_data['consti'], character_data['intel'], character_data['wisdom'],
            character_data['charisma'], character_data['armor'], character_data['initi'], character_data['desloc'],
            character_data['hp'], character_data['mana'], character_data['b_proef'], character_data['inspiration']
        )
        if self._execute_query(query, values):
            mycursor = self.db.cursor()
            mycursor.execute("SELECT LAST_INSERT_ID()")
            return mycursor.fetchone()[0]
        return 0

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
                "class": result[0][4],
                "img_link": result[0][5],
                "race": result[0][6],
                "money": result[0][7],
                "force": result[0][8],
                "dest": result[0][9],
                "consti": result[0][10],
                "intel": result[0][11],
                "wisdom": result[0][12],
                "charisma": result[0][13],
                "armor": result[0][14],
                "initi": result[0][15],
                "desloc": result[0][16],
                "hp": result[0][17],
                "mana": result[0][18],
                "b_proef": result[0][19],
                "inspiration": result[0][20]
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