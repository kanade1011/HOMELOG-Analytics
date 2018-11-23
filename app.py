from flask import Flask, render_template, request, redirect, url_for
from flask_httpauth import HTTPBasicAuth
from pymongo import MongoClient
from api import register, result_getter
from view import view

app = Flask(__name__)
app.config.update({'DEBUG': True})
auth = HTTPBasicAuth()
modules_define = [register.register, result_getter.api, view.view]
for applicaton in modules_define:
    app.register_blueprint(applicaton)


@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        # リクエストフォームから「名前」を取得して
        name = request.form['name']
        # index.html をレンダリングする
        return render_template('index.html')
    else:
        # エラーなどでリダイレクトしたい場合はこんな感じで
        return redirect(url_for('index'))


def create_collection():
    client = MongoClient('localhost', 27017)
    db = client['analytic_database']
    collection = db['analytic_database']
    return collection


if __name__ == '__main__':
    app.run()
