from flask import request, jsonify, g
import jwt, os
from functools import wraps

def jwt_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.cookies.get('access_token')

        if not token:
            print("Token no encontrado en cookies")
            return jsonify({'error': 'Token requerido'}), 401

        try:
            payload = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=['HS256'])
            g.user_id = payload['user_id']
        except jwt.ExpiredSignatureError:
            print("Token expirado")
            return jsonify({'error': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            print("Token inválido")
            return jsonify({'error': 'Token inválido'}), 401

        return f(*args, **kwargs)
    return wrapper
