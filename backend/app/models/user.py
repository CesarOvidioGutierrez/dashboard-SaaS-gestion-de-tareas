from datetime import datetime, timedelta
from .. import db
import jwt
import os
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relación con las tareas
    tasks = db.relationship('Task', backref='owner', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def generate_token(self):
        """Genera un token JWT para el usuario"""
        payload = {
            'user_id': self.id,
            'username': self.username,
            'exp': datetime.utcnow() + timedelta(days=1)  # Token válido por 1 día
        }
        
        # Obtener la clave secreta del entorno o usar una predeterminada
        secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
        
        # Generar el token
        token = jwt.encode(payload, secret_key, algorithm='HS256')
        
        return token
    
    @staticmethod
    def verify_token(token):
        """Verifica un token JWT y devuelve el usuario correspondiente"""
        try:
            # Obtener la clave secreta del entorno o usar una predeterminada
            secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
            
            # Decodificar el token
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            
            # Obtener el usuario por ID
            user_id = payload['user_id']
            return User.query.get(user_id)
        
        except jwt.ExpiredSignatureError:
            # Token expirado
            return None
        except jwt.InvalidTokenError:
            # Token inválido
            return None
