from database import db
from datetime import datetime
from enum import Enum

# --- Enums para validación interna
class TaskStatus(Enum):
    PENDIENTE = 'pendiente'
    EN_PROGRESO = 'en progreso'
    TERMINADO = 'terminado'

class TaskPriority(Enum):
    BAJA = 'baja'
    MEDIA = 'media'
    ALTA = 'alta'

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    tasks = db.relationship('Task', backref='owner', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default=TaskStatus.PENDIENTE.value)
    priority = db.Column(db.String(10), default=TaskPriority.BAJA.value)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'created_at': self.created_at.isoformat(),
            'user_id': self.user_id
        }
