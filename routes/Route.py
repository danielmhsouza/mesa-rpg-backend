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


    def add_artifact(self, campaign_code: int, name: str, desc: str, category: int):

        if self.controller.add_artifact_to_campaign(campaign_code, name, desc, category):
            return jsonify({"message": "Artefato adicionado com sucesso!"}), 200
        return jsonify({"error": "Erro ao adicionar artefato"}), 500

    def get_artifacts(self, campaign_id: int):
        if not campaign_id:
            return jsonify({"error": "Parâmetro 'campaign_id' é obrigatório"}), 500
        artifacts = self.controller.get_artifacts(campaign_id)
        if artifacts:
            return jsonify({"artifacts": artifacts}), 200
        return jsonify({"error": "Erro ao buscar artefatos."}), 500

    def add_intem_to_inventory(self, character_id: int, artefact_id: int):
        if (character_id < 1) or (artefact_id < 1):
            return jsonify({"error": "IDs obrigatórios."}), 500

        response = self.controller.add_intem_to_inventory(character_id, artefact_id)
        if response:
            return jsonify(response), 200
        return jsonify({"Erro": "Impossível adicionar item ao inventário."}), 500

    def get_inventory(self, character_id: int):
        if not character_id:
            return jsonify({"error": "IDs obrigatórios."}), 500
        
        response = self.controller.get_inventory(character_id)
        if response:
            return jsonify(response), 200
        return jsonify({"Erro": "Impossível mostrar inventário"})