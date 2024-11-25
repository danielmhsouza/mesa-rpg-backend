from flask import Flask, request, jsonify
from controllers.Controller import Controller

class Route:
    def __init__(self, app: Flask):
        self.app = app
        self.controller = Controller()
        self.register_routes()

    def register_routes(self):
        """
        Registra todas as rotas da aplicação.
        """
        self.app.add_url_rule('/login', 'login', self.login, methods=['POST'])
        self.app.add_url_rule('/register', 'register', self.register, methods=['POST'])
        self.app.add_url_rule('/create_campaign', 'create_campaign', self.create_campaign, methods=['POST'])
        self.app.add_url_rule('/enter_campaign_as_master', 'enter_campaign_as_master', self.enter_campaign_as_master, methods=['POST'])
        self.app.add_url_rule('/enter_campaign_as_player', 'enter_campaign_as_player', self.enter_campaign_as_player, methods=['POST'])
        self.app.add_url_rule('/add_artifact', 'add_artifact', self.add_artifact, methods=['POST'])
        self.app.add_url_rule('/add_item_to_character', 'add_item_to_character', self.add_item_to_character, methods=['POST'])
        self.app.add_url_rule('/remove_item_from_character', 'remove_item_from_character', self.remove_item_from_character, methods=['POST'])

    def login(self):
        """
        Rota de login, onde o usuário envia e-mail e senha para autenticação.
        :return: Resposta JSON com o status da operação.
        """
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"error": "Email e senha são obrigatórios"}), 400

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

    def create_campaign(self):
        """
        Rota para criar uma nova campanha.
        :return: Resposta JSON com o status da operação.
        """
        data = request.get_json()
        name = data.get('name')
        desc = data.get('desc')
        freq = data.get('freq')
        img_link = data.get('img_link')

        if not name or not desc or not freq or not img_link:
            return jsonify({"error": "Todos os campos são obrigatórios"}), 400

        if self.controller.create_campaign(name, desc, freq, img_link):
            return jsonify({"message": "Campanha criada com sucesso!"}), 201
        return jsonify({"error": "Erro ao criar campanha"}), 500

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
