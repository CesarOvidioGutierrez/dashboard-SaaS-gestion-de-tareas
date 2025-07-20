from flask_marshmallow import Marshmallow
from marshmallow import fields
from ..models import User

# Inicializar Marshmallow
ma = Marshmallow()

# Esquema para el modelo User (para registro y respuestas)
class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True
    
    id = ma.auto_field(dump_only=True)
    username = ma.auto_field(required=True)
    email = ma.auto_field(required=True)
    password = fields.String(load_only=True, required=True)
    created_at = ma.auto_field(dump_only=True)
    updated_at = ma.auto_field(dump_only=True)


# Crear instancias de los esquemas
user_schema = UserSchema()