from routes.auth import auth_bp
from routes.clientes import clientes_bp
from routes.main import main_bp
from routes.servicos import servicos_bp
from routes.servicos_disponiveis import catalogo_bp
from routes.veiculos import veiculos_bp


def register_blueprints(app):
    """Registra todas as rotas. Ao criar uma entidade nova, adicione aqui."""
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(clientes_bp)
    app.register_blueprint(veiculos_bp)
    app.register_blueprint(catalogo_bp)
    app.register_blueprint(servicos_bp)
