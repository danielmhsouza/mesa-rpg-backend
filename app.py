from flask import Flask, request, jsonify
from routes.Route import Route
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
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

# Executa a aplicação se for o arquivo principal
if __name__ == "__main__":
    app.run(debug=True)
