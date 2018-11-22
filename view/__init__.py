from flask import Flask
from view import view

application = Flask(__name__)

modules_define = [view.view]
application.register_blueprint(view.view)