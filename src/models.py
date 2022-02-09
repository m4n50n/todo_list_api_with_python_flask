from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    label = db.Column(db.String(120), nullable=False)
    done = db.Column(db.Boolean, nullable=False, default=False)
        
    def __repr__(self):
        return '<Todo %r>' % f"id: {self.id} / date: {self.date} / label: {self.label} / done: {self.done}"

    def serialize(self):
        return {
            "id": self.id,
            "date": self.date,
            "label": self.label,
            "done": self.done
        }
    
    def get_all_todos(self):
        todos = Todo.query.all()
        print(todos)
        
        # Method 1
        todos_list = list(map(lambda todo: todo.serialize(), todos)) 

        # Method 2
        """ todos_list = []
        for todo in todos:
            todos_list.append(todo.serialize()) """
        
        # Method 3
        """ todos_list = [todo.serialize() for todo in todos] """

        return todos_list
