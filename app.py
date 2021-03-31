from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy #初期化
from datetime import datetime

app = Flask(__name__)
#todo.dbという名前のデータベースを設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
#dbの生成
db = SQLAlchemy(app)

#db.Modelを継承して、モデルを作る
class Post(db.Model):
    #column(表の縦の列)
    #id、基本的にいつも必要
    #整数値、主キー
    id=db.Column(db.Integer, primary_key=True)
    #タスクにつけるタイトル
    #30字以内の文字列、空欄ＮＧ
    title=db.Column(db.String(30),nullable=False)
    #タスクの詳細
    #100字以内の文字列、空欄ＯＫ
    detail=db.Column(db.String(100))
    #タスクの期限
    #日付型、空欄ＮＧ
    due=db.Column(db.DateTime,nullable=False)

#methodsでトップページでもPOSTを受けられる状態にする
@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        #データベースからすべての投稿を取り出している
        #締め切りに近い順
        posts=Post.query.order_by(Post.due).all()
        #トップページに投稿を渡す
        return render_template('index.html',posts=posts)
    else:
        #1.postされた内容を受け取る
        title=request.form.get('title')
        detail=request.form.get('detail')
        due=request.form.get('due')

        #dueを文字列型から日付型に
        due=datetime.strptime(due, '%Y-%m-%d')

        #2.new_postインスタンスを作る(データベースを作る)
        new_post=Post(title=title,detail=detail,due=due)

        #3.データベースに投稿を保存
        '''
        add 内容を追加
        commit 実際のデータベースに反映
        '''
        db.session.add(new_post)
        db.session.commit()
        return redirect('/')

#タスクを作る    
@app.route('/create')
def create():
    return render_template('create.html')

#詳細ページ
@app.route('/detail/<int:id>')
def read(id):
    #該当するidの投稿内容を取得し、detail.htmlに渡している
    post = Post.query.get(id)
    return render_template('detail.html',post=post)

#タスクの削除
@app.route('/delete/<int:id>')
def delete(id):
    post = Post.query.get(id)

    db.session.delete(post)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    post=Post.query.get(id)

    #GETメッソドのとき、今まで書かれていた内容を表示
    if request.method=='GET':
        return render_template('update.html', post=post)

    #POSTメソッドのとき、変更内容を更新
    else:
        post.title = request.form.get('title')
        post.detail = request.form.get('detail')
        post.due = datetime.strptime(request.form.get('due'), '%Y-%m-%d')

        db.session.commit()
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)