class APIError(Exception):
    """
    Excepción base para errores de API.
    
    Attributes:
        message: Mensaje descriptivo del error
        status_code: Código de estado HTTP
        payload: Información adicional opcional
    """
    
    def __init__(self, message, status_code=400, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload
    
    def __str__(self):
        return f"APIError({self.status_code}): {self.message}"


class ValidationAPIError(APIError):
    """
    Excepción específica para errores de validación.
    Extiende APIError con funcionalidad específica para validaciones.
    """
    
    def __init__(self, validation_errors, message="Error de validación"):
        super().__init__(message, 400, validation_errors)


class AuthenticationError(APIError):
    """
    Excepción para errores de autenticación.
    Se usa cuando las credenciales son inválidas o falta autenticación.
    """
    
    def __init__(self, message="Error de autenticación"):
        super().__init__(message, 401)


class AuthorizationError(APIError):
    """
    Excepción para errores de autorización.
    Se usa cuando el usuario no tiene permisos para realizar una acción.
    """
    
    def __init__(self, message="No tienes permisos para realizar esta acción"):
        super().__init__(message, 403)


class NotFoundError(APIError):
    """
    Excepción para recursos no encontrados.
    Más específica que un 404 genérico.
    """
    
    def __init__(self, resource_name="Recurso", resource_id=None):
        if resource_id:
            message = f"{resource_name} con ID {resource_id} no encontrado"
        else:
            message = f"{resource_name} no encontrado"
        super().__init__(message, 404)


class ConflictError(APIError):
    """
    Excepción para conflictos de datos.
    Se usa cuando hay duplicados o estados inconsistentes.
    """
    
    def __init__(self, message="Conflicto con los datos existentes"):
        super().__init__(message, 409) 