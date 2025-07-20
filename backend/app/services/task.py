from app.models import Task

from app.schemas.task_schema import tasks_schema, task_schema

from app import db

def get_tasks_by_user_id(user_id):
    tasks = Task.query.filter_by(user_id=user_id).all()
    return tasks_schema.dump(tasks)

def get_task(task_id):
    task = Task.query.get(task_id)
    return task_schema.dump(task)

def create_task(task_data, user_id):
    task = Task(**task_data, user_id=user_id)
    db.session.add(task)
    db.session.commit()
    return task_schema.dump(task)

def update_task(task_id, task_data):
    task = Task.query.get(task_id)
    if task:
        task.update(task_data)
        db.session.commit()
    
    return task_schema.dump(task)

def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return task_schema.dump(task)


