from functools import wraps
from flask import request, jsonify
from ..models.user import User

def token_required(f):
    """
    Decorador que verifica si el token JWT es válido.
    Se debe usar en rutas que requieren autenticación.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Obtener el token del encabezado Authorization
        auth_header = request.headers.get('Authorization')
        
        if auth_header:
            # Formato esperado: "Bearer <token>"
            parts = auth_header.split()
            if len(parts) == 2 and parts[0].lower() == 'bearer':
                token = parts[1]
        
        if not token:
            return jsonify({'error': 'Token de autenticación requerido'}), 401
        
        # Verificar el token y obtener el usuario
        current_user = User.verify_token(token)
        
        if not current_user:
            return jsonify({'error': 'Token inválido o expirado'}), 401
        
        # Pasar el usuario actual a la función decorada
        return f(current_user, *args, **kwargs)
    
    return decorated 