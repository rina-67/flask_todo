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
        posts=Post.query.all()
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
    
@app.route('/create')
def create():
    return render_template('create.html')

if __name__ == '__main__':
    app.run(debug=True)