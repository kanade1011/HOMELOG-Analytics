from flask import Flask
from services import register
from view import view

app = Flask(__name__)
app.config.update({'DEBUG': True})
modules_define = [register.register, view.view]
for applicaton in modules_define:
    app.register_blueprint(applicaton)

if __name__ == '__main__':
    app.run()
