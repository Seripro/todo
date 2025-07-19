from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger  # 変更点

app = Flask(__name__)
swagger = Swagger(app)  # 変更点

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
    """
    ToDoのリスト表示と新規作成
    ---
    get:
      summary: ToDoリストのページを取得
      description: 全てのToDoタスクを含むHTMLページを返します。
      responses:
        200:
          description: 成功。ToDoリストが描画されたHTMLページ。
    post:
      summary: 新しいToDoを追加
      description: フォームデータから新しいタスクを作成します。
      requestBody:
        required: true
        content:
          application/x-www-form-urlencoded:
            schema:
              type: object
              properties:
                task:
                  type: string
                  description: 新しいタスクの内容
      responses:
        302:
          description: 作成成功後、トップページにリダイレクトします。
    """
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
    """
    指定されたIDのToDoを削除
    ---
    get:
      summary: ToDoを削除
      description: 指定されたIDのToDoタスクをデータベースから削除します。
      parameters:
        - name: id
          in: path
          required: true
          description: 削除するToDoのID
          schema:
            type: integer
      responses:
        302:
          description: 削除成功後、トップページにリダイレクトします。
    """
    todo = Todo.query.get(id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)