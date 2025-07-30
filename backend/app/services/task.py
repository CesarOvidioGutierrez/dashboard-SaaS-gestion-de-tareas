from app.models import Task

from app.schemas.task_schema import tasks_schema, task_schema

from app import db

def get_tasks_by_user_id(user_id):
    tasks = Task.query.filter_by(user_id=user_id).all()
    return tasks_schema.dump(tasks)

def get_task(task):
    return task_schema.dump(task)

def create_task(task_data, user_id):
    task = Task(**task_data, user_id=user_id)
    db.session.add(task)
    db.session.commit()
    return task_schema.dump(task)

def update_task(task_data, task):
    """
    Actualiza los campos de una tarea existente con los datos proporcionados.

    Args:
        task_data (dict): Diccionario con los datos a actualizar.
        task (Task): Instancia de la tarea a modificar.

    Returns:
        dict: Tarea serializada después de la actualización.
    """
    for key, value in task_data.items():
        setattr(task, key, value)
    db.session.commit()
    return task_schema.dump(task)

def delete_task(task):
    """
    Elimina una tarea existente.

    Args:
        task (Task): Instancia de la tarea a eliminar.
    
    Returns:
        dict: Tarea serializada después de la eliminación.
    """
    db.session.delete(task)
    db.session.commit()
    return task_schema.dump(task)


