from flask import Flask, request, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask_cors import CORS
import os
from datetime import datetime, date, timedelta
import jwt
from functools import wraps
from sqlalchemy import case, or_
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, instance_relative_config=True)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Check if the DATABASE_URL environment variable is set
if 'DATABASE_URL' in os.environ:
    # If it is, use it for the database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'].replace("postgres://", "postgresql://", 1)
else:
    # Otherwise, fall back to using a local SQLite database
    app.config.from_mapping(
        SECRET_KEY='your-super-secret-key',
        SQLALCHEMY_DATABASE_URI='sqlite:///tasks.db',
    )

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

db = SQLAlchemy(app)
api = Api(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    priority = db.Column(db.String(20), nullable=False, default='Medium') # Urgency
    complexity = db.Column(db.String(20), nullable=False, default='Medium')
    completed = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.Date, nullable=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)

    @property
    def is_overdue(self):
        if self.due_date and self.due_date < date.today():
            return True
        return False

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]
        if not token:
            return {'message': 'Token is missing!'}, 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            g.current_user = User.query.get(data['user_id'])
        except:
            return {'message': 'Token is invalid!'}, 401
        return f(*args, **kwargs)
    return decorated

# API Resources
class UserRegister(Resource):
    def post(self):
        data = request.get_json()
        if User.query.filter_by(username=data['username']).first():
            return {"message": "User already exists"}, 400
        
        user = User(username=data['username'])
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        
        return {"message": "User created successfully"}, 201

class TaskListResource(Resource):
    @token_required
    def get(self):
        current_user = g.current_user
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        overdue_filter = request.args.get('overdue', None)
        urgency_filter = request.args.get('urgency', None)
        complexity_filter = request.args.get('complexity', None)

        query = Task.query.filter(Task.user_id == current_user.id)

        if overdue_filter == 'true':
            query = query.filter(Task.due_date < date.today())
        
        if urgency_filter:
            query = query.filter(Task.priority == urgency_filter)

        if complexity_filter:
            query = query.filter(Task.complexity == complexity_filter)

        tasks = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            "tasks": [{
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "priority": task.priority,
                "complexity": task.complexity,
                "completed": task.completed,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "is_overdue": task.is_overdue
            } for task in tasks.items],
            "total_pages": tasks.pages,
            "current_page": tasks.page,
            "has_next": tasks.has_next,
            "has_prev": tasks.has_prev
        })

    @token_required
    def post(self):
        current_user = g.current_user
        data = request.get_json()
        due_date_str = data.get('due_date')
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date() if due_date_str else None
        new_task = Task(
            title=data['title'],
            description=data.get('description'),
            priority=data.get('priority', 'Medium'),
            complexity=data.get('complexity', 'Medium'),
            due_date=due_date,
            user_id=current_user.id
        )
        db.session.add(new_task)
        db.session.commit()
        return {"message": "Task created successfully"}, 201

class TaskResource(Resource):
    @token_required
    def get(self, task_id):
        current_user = g.current_user
        task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
        return jsonify({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "priority": task.priority,
            "complexity": task.complexity,
            "completed": task.completed,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "is_overdue": task.is_overdue
        })

    @token_required
    def put(self, task_id):
        current_user = g.current_user
        task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
        data = request.get_json()
        task.title = data.get('title', task.title)
        task.description = data.get('description', task.description)
        task.priority = data.get('priority', task.priority)
        task.complexity = data.get('complexity', task.complexity)
        task.completed = data.get('completed', task.completed)
        due_date_str = data.get('due_date')
        if due_date_str:
            task.due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        db.session.commit()
        return {"message": "Task updated successfully"}

    @token_required
    def delete(self, task_id):
        current_user = g.current_user
        task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
        db.session.delete(task)
        db.session.commit()
        return {"message": "Task deleted successfully"}

class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        if user and user.check_password(data['password']):
            token = jwt.encode({
                'user_id': user.id,
                'exp' : datetime.utcnow() + timedelta(minutes = 30)
            }, app.config['SECRET_KEY'])
            return {'token': token}
        return {'message': 'Invalid credentials'}, 401

api.add_resource(UserRegister, '/register')
api.add_resource(TaskListResource, '/tasks')
api.add_resource(TaskResource, '/tasks/<int:task_id>')
api.add_resource(UserLogin, '/login')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)