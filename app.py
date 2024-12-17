from flask import Flask, request, jsonify
from routes.Route import Route
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}}, methods=["GET", "POST", "PUT", "DELETE"], allow_headers=["Content-Type", "Authorization"])
app.config['CORS_HEADERS'] = 'Content-Type'
route = Route()

@app.route('/cadastro', methods=['POST'])
def rt_register():
    data = request.get_json()
    name = data['name']
    email = data['email']
    password = data['password']
    conf_pass = data['conf_pass']
    return route.register(user_name=name, email=email, password=password, confirm_password=conf_pass)
    

@app.route('/login', methods=["POST"])
def rt_login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    print(f"\n\nemail: {email} senha: {password}\n\n")

    return route.login(email=email, password=password)

@app.route('/criar-campanha', methods=["POST"])
def rt_create_campaign():
    data = request.get_json()
    name = data['name']
    desc = data['desc']
    freq = data['freq']
    img_link = data['img_link']
    user_id = data["user_id"]

    return route.create_campaign(name=name, desc=desc, freq=freq, img_link=img_link, user_id=user_id)

@app.route('/campanhas-usuario', methods=["GET"])
def rt_campaigns():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "ID do usuário é obrigatório"}), 400
    return route.get_campaigns(user_id)

@app.route('/campanha', methods=["GET"])
def rt_campaign():
    id = int(request.args.get('id'))
    if not id:
        return jsonify({"error": "Código da campanha obrigatório"}), 400
    
    return route.get_campaign(id)

@app.route('/criar-personagem', methods=['POST'])
def rt_create_character():
    data = request.get_json()
    character = {
        "name": data["name"],
        "race": data["race"],
        "classe": data["classe"],
        "img_link": data["img_link"],
        "force": data["force"],
        "carisma": data["carisma"],
        "destreza": data["destreza"],
        "constituicao": data["constituicaio"],
        "inteligencia": data["inteligencia"],
        "sabedoria": data["sabedoria"],
        "armadura": data["armadura"],
        "iniciativa": data["iniciativa"],
        "deslocamento": data["deslocamento"],
        "pontos_vida": data["pontos_vida"],
        "bonus_proef": data["bonus_proef"],
        "inspiracao": data["inspiracao"]
    }
    id_camp = data["camp_id"]
    id_user = data["user_id"]
    return route.create_character(character, id_camp, id_user)

@app.route('/personagem', methods=['GET'])
def rt_get_personagem():
    campaign_id = request.args.get("campaign_id")
    user_id = request.args.get("user_id") if request.args.get("user_id") else 0

    # Validação dos parâmetros
    if not campaign_id:
        return jsonify({"error": "Parâmetro 'campaign_id' é obrigatório"}), 500

    try:
        campaign_id = int(campaign_id)
        user_id = int(user_id)
    except ValueError:
        return jsonify({"error": "Parâmetros devem ser números inteiros"}), 500

    return route.get_character(campaign_id, user_id)

@app.route('/artefato', methods=['GET'])
def rt_get_artifacts():
    """
    Rota para buscar artefatos (itens ou missões) de uma campanha específica.
    """
    try:
        campaign_id = request.args.get("campaign_id")

        if not campaign_id:
            return jsonify({"error": "O ID da campanha é obrigatório"}), 400

        artifacts = route.get_artifacts(int(campaign_id))

        if artifacts:
            return jsonify({"artifacts": artifacts}), 200
        else:
            return jsonify({"message": "Nenhum artefato encontrado para esta campanha."}), 404

    except Exception as e:
        print(f"Erro ao buscar artefatos: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500


# Executa a aplicação se for o arquivo principal
if __name__ == "__main__":
    app.run(debug=True)
