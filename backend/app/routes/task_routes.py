from flask import Blueprint, request, jsonify
from ..utils.auth import token_required
from ..decorators.task import task_ownership_required
import services.task as task_service
from ..exceptions import APIError

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
@task_ownership_required
def get_task(task):
    # La tarea ya viene validada por el decorator
    task_data = task_service.get_task(task)
    
    return jsonify(task_data)

# Crear una nueva tarea
@tasks_bp.route('/api/tasks', methods=['POST'])
@token_required
def create_task(current_user):
    # Obtener datos JSON
    json_data = request.get_json()
    if not json_data:
        raise APIError('No se proporcionaron datos', 400)
    
    # ValidationError se maneja automáticamente por el error handler centralizado
    task_data = task_service.create_task(json_data, current_user.id)
    
    # Se devuelve la tarea creada
    return jsonify(task_data), 201

# Actualizar una tarea existente
@tasks_bp.route('/api/tasks/<int:task_id>', methods=['PUT'])
@token_required
@task_ownership_required
def update_task(task):
    # La tarea ya viene validada por el decorator
    
    # Obtener datos JSON
    json_data = request.get_json()
    if not json_data:
        raise APIError('No se proporcionaron datos', 400)
    
    # ValidationError se maneja automáticamente por el error handler
    task_data = task_service.update_task(json_data, task)
            
    # Se devuelve la tarea actualizada
    return jsonify(task_data)

# Eliminar una tarea
@tasks_bp.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@token_required
@task_ownership_required
def delete_task(task):
    # La tarea ya viene validada por el decorator
    
    # Se elimina la tarea
    task_service.delete_task(task)
    
    return jsonify({'message': 'Tarea eliminada correctamente'}), 200
