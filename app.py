from datetime import datetime
from urllib import request
from flask import Flask, render_template, request, redirect
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

@app.route('/', methods=['GET', 'POST'])
def show_todos():
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']

        record = Todo(title=title, description=desc)
        db.session.add(record)
        db.session.commit()

    allTodo = Todo.query.all()
    print(allTodo)
    return render_template('index.html', allTodo=allTodo)

@app.route('/update/<int:id>', methods=["GET", "POST"])
def update(id):
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']

        todo = Todo.query.filter_by(id=id).first()
        todo.title = title
        todo.description = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    todo = Todo.query.filter_by(id=id).first()
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:id>')
def delete(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, port=8000)
