from flask_marshmallow import Marshmallow
from marshmallow import fields, validates, ValidationError
from .models import User, Task

# Inicializar Marshmallow
ma = Marshmallow()

# Esquema para el modelo Task
class TaskSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Task
        load_instance = True  # Permite deserializar a una instancia del modelo
    
    id = ma.auto_field(dump_only=True)  # Solo para serialización, no para carga
    title = ma.auto_field(required=True)
    description = ma.auto_field()
    status = ma.auto_field()
    priority = ma.auto_field()
    due_date = fields.DateTime(format="%Y-%m-%dT%H:%M:%S", allow_none=True)
    user_id = ma.auto_field(dump_only=True)  # Solo para serialización
    created_at = ma.auto_field(dump_only=True)
    updated_at = ma.auto_field(dump_only=True)
    
    # Validación personalizada para el estado
    @validates('status')
    def validate_status(self, value):
        valid_statuses = ['pendiente', 'en_progreso', 'completada']
        if value not in valid_statuses:
            raise ValidationError(f"Estado inválido. Debe ser uno de: {', '.join(valid_statuses)}")
    
    # Validación personalizada para la prioridad
    @validates('priority')
    def validate_priority(self, value):
        valid_priorities = ['baja', 'media', 'alta']
        if value not in valid_priorities:
            raise ValidationError(f"Prioridad inválida. Debe ser uno de: {', '.join(valid_priorities)}")

# Esquema para el modelo User (para registro y respuestas)
class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True
    
    id = ma.auto_field(dump_only=True)
    username = ma.auto_field(required=True)
    email = ma.auto_field(required=True)
    password = fields.String(load_only=True, required=True)  # Solo para carga, no para serialización
    created_at = ma.auto_field(dump_only=True)
    updated_at = ma.auto_field(dump_only=True)

# Esquema para login
class LoginSchema(ma.Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)

# Crear instancias de los esquemas
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
user_schema = UserSchema()
login_schema = LoginSchema() 