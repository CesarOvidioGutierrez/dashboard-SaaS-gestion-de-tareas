from flask import Blueprint, request, jsonify
from ..models import User
from .. import db
from datetime import datetime
from ..schemas import user_schema, login_schema
from marshmallow import ValidationError

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/auth/register', methods=['POST'])
def register():
    try:
        # Obtener datos JSON
        json_data = request.get_json()
        if not json_data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        # Validar datos usando el esquema
        user_data = user_schema.load(json_data)
        
        # Verificar si el usuario ya existe
        if User.query.filter_by(username=user_data.username).first():
            return jsonify({'error': 'El nombre de usuario ya está en uso'}), 409
        
        # Verificar si el email ya existe
        if User.query.filter_by(email=user_data.email).first():
            return jsonify({'error': 'El email ya está registrado'}), 409
        
        # Hashear la contraseña
        password = user_data.password_hash  # En realidad es el campo 'password' del JSON
        user_data.set_password(password)
        
        # Guardar en la base de datos
        db.session.add(user_data)
        db.session.commit()
        
        # Generar token para el nuevo usuario
        token = user_data.generate_token()
        
        # Serializar y devolver el usuario creado (sin la contraseña)
        user_response = user_schema.dump(user_data)
        user_response['token'] = token
        
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