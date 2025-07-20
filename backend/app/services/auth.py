from .. import db

from app.schemas.user_schema import user_schema, login_schema

from app.services.user import get_user_by_username, get_user_by_email

def register_user(json_data):
    user_data = user_schema.load(json_data)
    
    if get_user_by_username(user_data.username):
        raise ValueError("El nombre de usuario ya está en uso")
    
    if get_user_by_email(user_data.email):
        raise ValueError("El email ya está registrado")
    
    user_data.set_password(user_data.password)

    db.session.add(user_data)
    db.session.commit()

    user_response = user_schema.dump(user_data)
    token = user_data.generate_token()
    user_response['token'] = token

    return user_response

def login_user(json_data):
    login_data = login_schema.load(json_data)

    user = get_user_by_username(login_data['username'])
    if not user or not user.check_password(login_data['password']):
        raise ValueError("Credenciales inválidas")
        
    token = user.generate_token()
    user_response = user_schema.dump(user)
    user_response['token'] = token

    return user_response