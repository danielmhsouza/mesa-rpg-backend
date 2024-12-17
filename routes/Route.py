from flask import request, jsonify
from controllers.Controller import Controller

class Route:
    def __init__(self):
        self.controller = Controller()

    
    def login(self, email, password):
        """
        Rota de login, onde o usuário envia e-mail e senha para autenticação.
        :return: Resposta JSON com o status da operação.
        """

        if not email or not password:
            return jsonify({"error": "Email e senha são obrigatórios"}), 500

        user_data = self.controller.login(email, password)
        if user_data:
            return jsonify(user_data), 200
        return jsonify({"error": "Credenciais inválidas"}), 401

    def register(self, user_name, email, password, confirm_password):
        """
        Rota de registro, onde o usuário cria uma conta.
        :return: Resposta JSON com o status da operação.
        """

        if not user_name or not email or not password or not confirm_password:
            return jsonify({"error": "Todos os campos são obrigatórios"}), 500
        
        if password != confirm_password:
            return jsonify({"error": "As senhas não coincidem"}), 500

        if self.controller.register(user_name, email, password, confirm_password):
            return jsonify({"message": "Usuário registrado com sucesso!"}), 200
        return jsonify({"error": "Erro ao registrar usuário"}), 500

    def get_campaigns(self, user_id: int):
        campaigns = self.controller.get_campaigns(user_id)
        if campaigns:
            return jsonify(campaigns), 200
        return jsonify({"msg": "Nenhuma campanha encontrada."}), 404

    def get_campaign(self, id: int):
        campaign = self.controller.get_campaign(id)
        if campaign:
            return jsonify(campaign), 200
        return jsonify({"msg": "Nenhuma campanha encontrada."}), 404

    def create_campaign(self, name, desc, freq, img_link, user_id):
        """
        Rota para criar uma nova campanha.
        :return: Resposta JSON com o status da operação.
        """

        if not name or not desc or not freq:
            return jsonify({"error": "Nome, descrição e frequência sâo obrigatórios!"}), 500

        if self.controller.create_campaign(name, desc, freq, img_link, user_id):
            return jsonify({"message": "Campanha criada com sucesso!"}), 200
        return jsonify({"error": "Erro ao criar campanha"}), 500

    def create_character(self, character: dict, id_camp: int, id_user: int):
        character = self.controller.create_character(character, id_camp, id_user)
        if character < 1:
            return jsonify({"error": "Erro ao criar personagem!"}), 500
        
        campaign = self.controller.insert_entry_campaign(id_camp, id_user)
        if campaign < 1:
            self.controller.delete_character(character)
            return jsonify({"error": "Erro ao entrar na campanha!"}), 500
        
        return jsonify({"message": f"Você entrou na campanha {campaign} com o personagem {character}!"}), 200
        
    def get_character(self, campaign_id: int, user_id: int):
        if not campaign_id:
            return jsonify({"error": "Parâmetros 'campaign_id' e 'user_id' são obrigatórios"}), 500
        if user_id != 0:
            character = self.controller.get_characters_by_campaign_and_user(campaign_id, user_id)
        else:
            character = self.controller.get_all_character_by_campaign(campaign_id)
            
        if character:
            return jsonify({"characters": character}), 200
        return jsonify({"message": "Nenhum personagem encontrado"}), 500

    def enter_campaign_as_master(self):
        """
        Rota para o usuário entrar em uma campanha como mestre.
        :return: Resposta JSON com o status da operação.
        """
        data = request.get_json()
        code = data.get('code')

        if not code:
            return jsonify({"error": "Código da campanha é obrigatório"}), 400

        campaign_data = self.controller.enter_campaign_as_master(code)
        if campaign_data:
            return jsonify(campaign_data), 200
        return jsonify({"error": "Erro ao entrar na campanha como mestre"}), 500

    def enter_campaign_as_player(self):
        """
        Rota para o usuário entrar em uma campanha como jogador.
        :return: Resposta JSON com o status da operação.
        """
        data = request.get_json()
        code = data.get('code')

        if not code:
            return jsonify({"error": "Código da campanha é obrigatório"}), 400

        campaign_data = self.controller.enter_campaign_as_player(code)
        if campaign_data:
            return jsonify(campaign_data), 200
        return jsonify({"error": "Erro ao entrar na campanha como jogador"}), 500

    def add_artifact(self):
        """
        Rota para adicionar um artefato à campanha.
        :return: Resposta JSON com o status da operação.
        """
        data = request.get_json()
        campaign_code = data.get('campaign_code')
        name = data.get('name')
        desc = data.get('desc')
        category = data.get('category')

        if not campaign_code or not name or not desc or not category:
            return jsonify({"error": "Todos os campos são obrigatórios"}), 400

        if self.controller.add_artifact_to_campaign(campaign_code, name, desc, category):
            return jsonify({"message": "Artefato adicionado com sucesso!"}), 201
        return jsonify({"error": "Erro ao adicionar artefato"}), 500

    def get_artifacts(self, campaign_id: int):
        if not campaign_id:
            return jsonify({"error": "Parâmetro 'campaign_id' é obrigatório"}), 500
        artifacts = self.controller.get_artifacts(campaign_id)
        if artifacts:
            return jsonify({"artifacts": artifacts}), 200
        return jsonify({"error": "Erro ao buscar artefatos."}), 500


    def add_item_to_character(self):
        """
        Rota para adicionar um artefato ao personagem.
        :return: Resposta JSON com o status da operação.
        """
        data = request.get_json()
        artifact_code = data.get('artifact_code')
        character_code = data.get('character_code')

        if not artifact_code or not character_code:
            return jsonify({"error": "Código do artefato e personagem são obrigatórios"}), 400

        if self.controller.add_item_to_character(artifact_code, character_code):
            return jsonify({"message": "Item adicionado ao personagem com sucesso!"}), 200
        return jsonify({"error": "Erro ao adicionar item ao personagem"}), 500

    def remove_item_from_character(self):
        """
        Rota para remover um artefato do inventário do personagem.
        :return: Resposta JSON com o status da operação.
        """
        data = request.get_json()
        artifact_code = data.get('artifact_code')
        character_code = data.get('character_code')

        if not artifact_code or not character_code:
            return jsonify({"error": "Código do artefato e personagem são obrigatórios"}), 400

        if self.controller.remove_item_from_character(artifact_code, character_code):
            return jsonify({"message": "Item removido do personagem com sucesso!"}), 200
        return jsonify({"error": "Erro ao remover item do personagem"}), 500


