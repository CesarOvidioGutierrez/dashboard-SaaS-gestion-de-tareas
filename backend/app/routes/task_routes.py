from flask import Blueprint, request, jsonify
from ..models import Task
from ..utils.auth import token_required
import services.task as task_service
from marshmallow import ValidationError

tasks_bp = Blueprint('tasks', __name__)

# Obtener todas las tareas
@tasks_bp.route('/api/tasks', methods=['GET'])
@token_required
def get_tasks(current_user):
    # Obtener solo las tareas del usuario actual y serializarlas
    tasks = task_service.get_tasks_by_user_id(current_user.id)
    
    return jsonify(tasks)

# Obtener una tarea específica
@tasks_bp.route('/api/tasks/<int:task_id>', methods=['GET'])
@token_required
def get_task(current_user, task_id):
    # Obtener la tarea y verificar que pertenezca al usuario actual
    task = task_service.get_task(task_id)
    
    if task.user_id != current_user.id:
        return jsonify({'error': 'No autorizado para acceder a esta tarea'}), 403
    
    return jsonify(task)

# Crear una nueva tarea
@tasks_bp.route('/api/tasks', methods=['POST'])
@token_required
def create_task(current_user):
    try:
        # Obtener datos JSON
        json_data = request.get_json()
        if not json_data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        # Se crea la tarea y se asigna el usuario actual como propietario, además se serializa la tarea
        task_data = task_service.create_task(json_data, current_user.id)
        
        # Se devuelve la tarea creada
        return jsonify(task_data), 201
        
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
        
        # Se actualiza la tarea
        task_data = task_service.update_task(json_data, task_id)
                
        # Se devuelve la tarea actualizada
        return jsonify(task_data)
        
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
    
    # Se elimina la tarea
    task_service.delete_task(task_id)
    
    return jsonify({'message': 'Tarea eliminada correctamente'}), 200
