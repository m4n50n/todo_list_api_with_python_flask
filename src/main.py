"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from datetime import datetime
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Todo
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_CONNECTION_STRING")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route("/")
def sitemap():
    return generate_sitemap(app)

@app.route("/todos", methods=["GET"])
def get_all_todos():
    t = Todo() # create new class instance
    return jsonify(t.get_all_todos()), 200

@app.route("/todos/<int:todo_id>", methods=["GET"])
def get_todo(todo_id):
    todo = Todo.query.get(todo_id)

    if todo == None:
        response = f"There is no task with ID '{todo_id}'"
    else:
        response = todo.serialize()

    return jsonify(response), 200

@app.route("/todos/add_todo", methods=["POST"])
def add_todo():
    body = request.get_json()
    new_todo = Todo(label=body["label"], date=datetime.now())
    db.session.add(new_todo)
    db.session.commit()

    return jsonify(f"A new todo is added!! {new_todo.serialize()}"), 200

@app.route("/todos/delete_todo/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    todo = Todo.query.get(todo_id)

    if todo == None:
        return f"There is no task with ID '{todo_id}'"
    else:
        Todo.query.filter_by(id=todo_id).delete()
        db.session.commit()

        return jsonify(f"Todo with ID '{todo_id}' has been deleted!!"), 200 

# this only runs if `$ python src/main.py` is executed
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=PORT, debug=False)
