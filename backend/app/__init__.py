from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from .config import config
from .error_handlers import register_error_handlers
# Inicializar extensiones
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name=None):
    """
    Factory pattern para crear la aplicación Flask.
    
    Args:
        config_name: Nombre de la configuración a usar (development, testing, production)
        
    Returns:
        app: Instancia configurada de Flask
    """
    # Si no se especifica configuración, usar la variable de entorno o default
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    CORS(app)
    
    # Cargar configuración
    app.config.from_object(config[config_name])
    
    # Inicializar extensiones con la aplicación
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Inicializar Marshmallow
    from .schemas import ma
    ma.init_app(app)
    
    # Rutas básicas de salud
    @app.route('/api/health')
    def health():
        return {'status': 'healthy'}, 200
    
    @app.route('/api/hello')
    def hello():
        return {'message': 'Hola desde el backend de Flask!'}, 200
    
    # Importar modelos para que Flask-Migrate los detecte
    from .models import User, Task
    
    # Importar y registrar blueprints
    from .routes import tasks_bp, auth_bp
    app.register_blueprint(tasks_bp)
    app.register_blueprint(auth_bp)
    
    # Registrar error handlers centralizados
    register_error_handlers(app)
    
    return app
