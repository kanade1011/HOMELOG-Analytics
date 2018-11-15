from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import services.batch_service as service

app = Flask(__name__)


@app.route('/')
def index():
    title = "index"
    str = "foo"
    return render_template('index.html', str=str, title=title)


@app.route('/post', methods=['GET', 'POST'])
def post():
    title = "こんにちは"
    if request.method == 'POST':
        # リクエストフォームから「名前」を取得して
        name = request.form['name']
        # index.html をレンダリングする
        return render_template('index.html',
                               name=name, title=title)
    else:
        # エラーなどでリダイレクトしたい場合はこんな感じで
        return redirect(url_for('index'))


def create_collection():
    client = MongoClient('localhost', 27017)
    db = client['analytic_database']
    collection = db['analytic_database']
    return collection


collection = create_collection()
post = service.create_collection()

collection.insert_one(post)

record = collection.find_one({"month": "10"})
print(record['body'])

if __name__ == '__main__':
    app.run(host='0.0.0.0')