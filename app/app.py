from flask import Flask
from routes.Route import Route

def create_app():
    """
    Função que cria e configura a aplicação Flask.
    """
    # Cria a instância da aplicação Flask
    app = Flask(__name__)

    # Configura as rotas
    Route(app)

    return app

# Executa a aplicação se for o arquivo principal
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
