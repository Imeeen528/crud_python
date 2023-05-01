from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todos(db.Model):
    __tablename__ = 'todos'
    _id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Todo {self.title}>"

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['description']
        todo = Todos(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    all_todos = Todos.query.all() #fetch todos from db in html
    return render_template('index.html', todos=all_todos)

@app.route('/delete/<int:_id>')
def delete(_id):
    todo = Todos.query.filter_by(_id=_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:_id>', methods=['POST', 'GET'])
def update(_id):
    todo = Todos.query.filter_by(_id=_id).first()
    if request.method == 'POST':
        todo.title = request.form['title']
        todo.desc = request.form['description']
        db.session.commit()
        return redirect('/')
    return render_template('update.html', todo=todo)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

