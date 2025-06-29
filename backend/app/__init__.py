from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    @app.route('/api/health')
    def health():
        return {'status': 'healthy'}, 200
    
    @app.route('/api/hello')
    def hello():
        return {'message': 'Hola desde el backend de Flask!'}, 200
    
    return app
