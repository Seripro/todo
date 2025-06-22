from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

# モデル定義（テーブルの設計）
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)

# 初回だけDB作成
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        task = request.form.get('task')
        if task:
            new_todo = Todo(task=task)
            db.session.add(new_todo)
            db.session.commit()
        return redirect('/')
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)

@app.route('/delete/<int:id>')
def delete(id):
    todo = Todo.query.get(id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
