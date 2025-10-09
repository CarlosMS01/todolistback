# backend/routes/tasks.py
from flask import Blueprint, request, jsonify, g
from backend.models import Task
from backend.database import db
from backend.middleware.jwt_required import jwt_required

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/tasks', methods=['POST'])
@jwt_required
def create_task():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description', '')
    status = data.get('status', 'pendiente')
    priority = data.get('priority', 'media')

    new_task = Task(
        title=title,
        description=description,
        status=status,
        priority=priority,
        user_id=g.user_id
    )
    db.session.add(new_task)
    db.session.commit()

    return jsonify({'message': 'Tarea creada correctamente'})

@tasks_bp.route('/tasks', methods=['GET'])
@jwt_required
def get_tasks():
    tasks = Task.query.filter_by(user_id=g.user_id).all()
    result = [t.to_dict() for t in tasks]

    return jsonify(result)

@tasks_bp.route('/tasks/<int:id>', methods=['GET'])
@jwt_required
def get_task(id):
    task = Task.query.filter_by(id=id, user_id=g.user_id).first()
    if not task:
        return jsonify({'error': 'Tarea no encontrada'}), 404
    
    return jsonify(task.to_dict()), 200

@tasks_bp.route('/tasks/<int:id>', methods=['PUT'])
@jwt_required
def update_task(id):
    task = Task.query.filter_by(id=id, user_id=g.user_id).first()
    if not task:
        return jsonify({'error': 'Tarea no encontrada'}), 404

    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.status = data.get('status', task.status)
    task.priority = data.get('priority', task.priority)

    db.session.commit()
    return jsonify({'message': 'Tarea actualizada'})

@tasks_bp.route('/tasks/<int:id>', methods=['DELETE'])
@jwt_required
def delete_task(id):
    task = Task.query.filter_by(id=id, user_id=g.user_id).first()
    if not task:
        return jsonify({'error': 'Tarea no encontrada'}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Tarea eliminada'})
