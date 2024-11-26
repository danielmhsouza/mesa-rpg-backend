from flask import Flask, request
from routes.Route import Route

app = Flask(__name__)

# Configura as rotas
Route(app)

@app.route('/cadastro', methods=['POST'])
def register():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    conf_pass = request.form.get('conf_pass')
    return Route.register(name, email, password, conf_pass)
    


# Executa a aplicação se for o arquivo principal
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
