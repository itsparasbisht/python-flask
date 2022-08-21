from datetime import datetime
import json
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.id} {self.title}"

@app.route('/')
def hello_world():
    record = Todo(title='first todo', description='a test description')
    db.session.add(record)
    db.session.commit()
    return render_template('index.html')

@app.route('/show-todos')
def show_todos():
    data = Todo.query.all()
    print(data)
    return "show todos"
    # return json.dumps(data, indent=4)

if __name__ == "__main__":
    app.run(debug=True, port=8000)
