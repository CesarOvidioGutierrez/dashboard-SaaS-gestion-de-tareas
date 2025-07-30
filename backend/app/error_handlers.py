from flask import jsonify, request, current_app
from marshmallow import ValidationError
from datetime import datetime
import logging

from .exceptions import APIError


def register_error_handlers(app):
    """
    Registra todos los error handlers en la aplicación Flask.
    
    Args:
        app: Instancia de la aplicación Flask
    """
    
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        """
        Maneja errores de validación de Marshmallow.
        
        Args:
            error: Instancia de ValidationError de Marshmallow
            
        Returns:
            tuple: (response_json, status_code)
        """
        # Logging estructurado para debugging
        current_app.logger.warning(
            f"Validation error - Endpoint: {request.endpoint} | "
            f"Method: {request.method} | "
            f"Fields with errors: {len(error.messages)}"
        )
        
        # Formatear errores para respuesta user-friendly
        formatted_errors = _format_validation_errors(error.messages)
        
        response = {
            'success': False,
            'error': {
                'type': 'validation_error',
                'message': 'Los datos proporcionados contienen errores',
                'fields': formatted_errors
            },
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
        
        return jsonify(response), 400
    
    @app.errorhandler(APIError)
    def handle_api_error(error):
        """
        Maneja errores personalizados de la API.
        
        Args:
            error: Instancia de APIError personalizada
            
        Returns:
            tuple: (response_json, status_code)
        """
        # Logging con nivel apropiado según el status code
        log_level = 'error' if error.status_code >= 500 else 'warning'
        
        getattr(current_app.logger, log_level)(
            f"API Error - Status: {error.status_code} | "
            f"Message: {error.message} | "
            f"Endpoint: {request.endpoint}"
        )
        
        response = {
            'success': False,
            'error': {
                'type': 'api_error',
                'message': error.message,
                'code': error.status_code
            },
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
        
        # Agregar detalles adicionales si existen
        if error.payload:
            response['error']['details'] = error.payload
            
        return jsonify(response), error.status_code
    
    @app.errorhandler(404)
    def handle_not_found(error):
        """
        Maneja errores 404 - Recurso no encontrado.
        
        Args:
            error: Error 404 de Flask
            
        Returns:
            tuple: (response_json, status_code)
        """
        current_app.logger.info(f"404 Not Found - Path: {request.path}")
        
        response = {
            'success': False,
            'error': {
                'type': 'not_found',
                'message': 'El recurso solicitado no fue encontrado',
                'code': 404
            },
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
        
        return jsonify(response), 404
    
    @app.errorhandler(500)
    def handle_internal_error(error):
        """
        Maneja errores internos del servidor.
        
        Args:
            error: Error 500 de Flask
            
        Returns:
            tuple: (response_json, status_code)
        """
        current_app.logger.error(
            f"Internal Server Error - Endpoint: {request.endpoint} | "
            f"Error: {str(error)}"
        )
        
        response = {
            'success': False,
            'error': {
                'type': 'internal_error',
                'message': 'Error interno del servidor',
                'code': 500
            },
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
        
        return jsonify(response), 500


def _format_validation_errors(messages):
    """
    Formatea los errores de validación de Marshmallow.
    Convierte errores técnicos en mensajes user-friendly.
    
    Args:
        messages: Dict con errores de Marshmallow
        
    Returns:
        dict: Errores formateados para el usuario
    """
    formatted = {}
    
    for field, errors in messages.items():
        if isinstance(errors, list):
            # Tomar el primer error y traducirlo si es posible
            formatted[field] = _translate_error_message(errors[0] if errors else 'Campo inválido')
        elif isinstance(errors, dict):
            # Errores anidados (para objetos complejos)
            formatted[field] = _format_validation_errors(errors)
        else:
            formatted[field] = _translate_error_message(str(errors))
    
    return formatted


def _translate_error_message(technical_error):
    """
    Traduce errores técnicos a mensajes amigables para el usuario.
    
    Args:
        technical_error: Mensaje técnico de Marshmallow
        
    Returns:
        str: Mensaje amigable para el usuario
    """
    error_translations = {
        'Missing data for required field.': 'Este campo es obligatorio',
        'Not a valid string.': 'Debe ser un texto válido',
        'Not a valid integer.': 'Debe ser un número entero',
        'Not a valid email address.': 'Debe ser un email válido',
        'Field may not be null.': 'Este campo no puede estar vacío',
        'Not a valid datetime.': 'Formato de fecha inválido',
        'Not a valid boolean.': 'Debe ser verdadero o falso'
    }
    
    return error_translations.get(technical_error, technical_error) 