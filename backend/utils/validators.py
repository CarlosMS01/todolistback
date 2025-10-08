# app/utils/validators.py
from flask import request
import os
import jwt
from models import User

def get_current_user():
    token = request.cookies.get('access_token')
    if not token:
        return None

    try:
        payload = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=['HS256'])
        user_id = payload.get('user_id')
        return User.query.get(user_id)
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
