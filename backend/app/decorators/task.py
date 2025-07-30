from flask import jsonify
from functools import wraps
from app.models.task import Task

def task_ownership_required(handler):
    """
    Decorator que valida que el usuario actual sea el propietario de la tarea
    antes de ejecutar el handler del endpoint.
    
    Args:
        handler: Función del endpoint que maneja la request
        
    Returns:
        Función decorada que incluye validación de ownership
        
    Raises:
        404: Si la tarea no existe
        403: Si el usuario no es propietario de la tarea
    """
    @wraps(handler)
    def decorated(current_user, task_id, *args, **kwargs):
        # Validar existencia de la tarea
        task = Task.query.get_or_404(task_id)
        
        # Validar ownership
        if task.user_id != current_user.id:
            return jsonify({
                'error': 'No autorizado para acceder a esta tarea'
            }), 403
        
        # Ejecutar el handler original con la tarea validada
        return handler(current_user, task_id, task, *args, **kwargs)
    
    return decorated