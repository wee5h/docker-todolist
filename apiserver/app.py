from flask import Flask, jsonify, request 
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import os

user = os.getenv('MYSQL_USER')
db_pass = os.getenv('MYSQL_PASSWORD')
db_name = os.getenv('MYSQL_DATABASE')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{user}:{db_pass}@db:3306/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {"id": self.id, "task": self.task}

@app.route('/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    return jsonify([todo.to_dict() for todo in todos])

@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo_by_id(todo_id):
    todo = Todo.query.get(todo_id)
    if todo:
        return jsonify(todo.to_dict())
    return jsonify({"error": "Todo not found"}), 404

@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.json
    new_todo = Todo(task=data['task'])
    db.session.add(new_todo)
    db.session.commit()
    #201 means created. it is what's responded to the website calling this api. 
    return jsonify(new_todo.to_dict()), 201

@app.route('/todos/<int:todo_id>', methods=['POST'])
def del_todo_by_id(todo_id):
    todo = Todo.query.get(todo_id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
        #200 OK is a succesful response code, indicates request has succeeded
        return jsonify({"message": f'{todo.task} has been successfully deleted.'}), 200
    return jsonify({"error": f'todo {todo_id} not found.'}), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
