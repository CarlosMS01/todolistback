from flask import Blueprint, request, jsonify, make_response, g
from backend.models import User
from backend.database import db
from flask_bcrypt import Bcrypt
import jwt, os
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()

def decode_token(token):
    try:
        payload = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expirado")
    except jwt.InvalidTokenError:
        raise ValueError("Token inválido")

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'Todos los campos son obligatorios'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email ya registrado'}), 400

    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, email=email, password_hash=hashed_pw)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Usuario registrado correctamente'})

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({'error': 'Credenciales inválidas'}), 401

    payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(hours=2)
    }
    token = jwt.encode(payload, os.getenv('JWT_SECRET'), algorithm='HS256')

    response = make_response(jsonify({'message': 'Login exitoso'}))
    response.set_cookie(
        'access_token',
        token,
        httponly=True,
        secure=True,
        samesite='None',
        max_age=7200
    )
    return response

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    token = request.cookies.get('access_token')
    if not token:
        return jsonify({'error': 'Token requerido'}), 401

    try:
        payload = decode_token(token)
        user = User.query.get(payload['user_id'])
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        g.user = user
        return jsonify(user.to_dict())
    except ValueError as e:
        return jsonify({'error': str(e)}), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    response = jsonify({'message': 'Sesión cerrada'})
    response.set_cookie(
        'access_token',
        '',
        httponly=True,
        secure=True,
        samesite='None',
        max_age=0
    )
    return response

