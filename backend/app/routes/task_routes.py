from flask import Blueprint, request, jsonify
from ..models import Task, User
from .. import db
from datetime import datetime
from ..utils.auth import token_required
from ..schemas import task_schema, tasks_schema
from marshmallow import ValidationError

tasks_bp = Blueprint('tasks', __name__)

# Obtener todas las tareas
@tasks_bp.route('/api/tasks', methods=['GET'])
@token_required
def get_tasks(current_user):
    # Obtener solo las tareas del usuario actual
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    
    # Serializar las tareas usando el esquema
    return jsonify(tasks_schema.dump(tasks))

# Obtener una tarea específica
@tasks_bp.route('/api/tasks/<int:task_id>', methods=['GET'])
@token_required
def get_task(current_user, task_id):
    # Obtener la tarea y verificar que pertenezca al usuario actual
    task = Task.query.get_or_404(task_id)
    
    if task.user_id != current_user.id:
        return jsonify({'error': 'No autorizado para acceder a esta tarea'}), 403
    
    # Serializar la tarea usando el esquema
    return jsonify(task_schema.dump(task))

# Crear una nueva tarea
@tasks_bp.route('/api/tasks', methods=['POST'])
@token_required
def create_task(current_user):
    try:
        # Obtener datos JSON
        json_data = request.get_json()
        if not json_data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        # Validar y deserializar los datos usando el esquema
        # Nota: load_instance=True en el esquema permite crear una instancia del modelo
        task_data = task_schema.load(json_data)
        
        # Asignar el usuario actual como propietario
        task_data.user_id = current_user.id
        
        # Guardar en la base de datos
        db.session.add(task_data)
        db.session.commit()
        
        # Serializar y devolver la tarea creada
        return jsonify(task_schema.dump(task_data)), 201
        
    except ValidationError as err:
        # Manejar errores de validación
        return jsonify({'error': 'Error de validación', 'details': err.messages}), 400

# Actualizar una tarea existente
@tasks_bp.route('/api/tasks/<int:task_id>', methods=['PUT'])
@token_required
def update_task(current_user, task_id):
    # Obtener la tarea existente
    task = Task.query.get_or_404(task_id)
    
    # Verificar que la tarea pertenezca al usuario actual
    if task.user_id != current_user.id:
        return jsonify({'error': 'No autorizado para modificar esta tarea'}), 403
    
    try:
        # Obtener datos JSON
        json_data = request.get_json()
        if not json_data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        # Validar datos parciales (solo los campos proporcionados)
        # Partial=True permite actualización parcial
        task_data = task_schema.load(json_data, instance=task, partial=True)
        
        # No es necesario asignar los campos individualmente porque
        # load con instance=task actualiza el objeto directamente
        
        # Actualizar fecha de modificación
        task.updated_at = datetime.utcnow()
        
        # Guardar cambios
        db.session.commit()
        
        # Serializar y devolver la tarea actualizada
        return jsonify(task_schema.dump(task))
        
    except ValidationError as err:
        # Manejar errores de validación
        return jsonify({'error': 'Error de validación', 'details': err.messages}), 400

# Eliminar una tarea
@tasks_bp.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@token_required
def delete_task(current_user, task_id):
    task = Task.query.get_or_404(task_id)
    
    # Verificar que la tarea pertenezca al usuario actual
    if task.user_id != current_user.id:
        return jsonify({'error': 'No autorizado para eliminar esta tarea'}), 403
    
    db.session.delete(task)
    db.session.commit()
    
    return jsonify({'message': 'Tarea eliminada correctamente'}), 200
