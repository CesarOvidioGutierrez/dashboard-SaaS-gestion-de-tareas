from flask import Blueprint, request, jsonify
from ..models import User
from ..schemas import user_schema, login_schema
from marshmallow import ValidationError
from app.services.auth import register_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/auth/register', methods=['POST'])
def register():
    try:
        # Obtener datos JSON
        json_data = request.get_json()
        if not json_data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400

        # Registrar usuario 
        user_response = register_user(json_data)
        
        return jsonify({
            'message': 'Usuario registrado exitosamente',
            'user': user_response
        }), 201
        
    except ValidationError as err:
        # Manejar errores de validación
        return jsonify({'error': 'Error de validación', 'details': err.messages}), 400

@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    try:
        # Obtener datos JSON
        json_data = request.get_json()
        if not json_data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        # Validar datos usando el esquema de login
        login_data = login_schema.load(json_data)
        
        # Buscar usuario por nombre de usuario
        user = User.query.filter_by(username=login_data['username']).first()
        
        # Verificar si el usuario existe y la contraseña es correcta
        if not user or not user.check_password(login_data['password']):
            return jsonify({'error': 'Credenciales inválidas'}), 401
        
        # Generar token para el usuario
        token = user.generate_token()
        
        # Serializar y devolver el usuario (sin la contraseña)
        user_response = user_schema.dump(user)
        user_response['token'] = token
        
        return jsonify({
            'message': 'Inicio de sesión exitoso',
            'user': user_response
        })
        
    except ValidationError as err:
        # Manejar errores de validación
        return jsonify({'error': 'Error de validación', 'details': err.messages}), 400 