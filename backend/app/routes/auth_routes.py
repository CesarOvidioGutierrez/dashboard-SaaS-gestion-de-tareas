from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.services.auth import register_user, login_user

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
        user_response = login_user(json_data)
        
        return jsonify({
            'message': 'Inicio de sesión exitoso',
            'user': user_response
        })
        
    except ValidationError as err:
        # Manejar errores de validación
        return jsonify({'error': 'Error de validación', 'details': err.messages}), 400 