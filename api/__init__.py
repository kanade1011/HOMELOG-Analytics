from flask import Flask
from api import register, result_getter

application = Flask(__name__)

modules_define = [register.register, result_getter.api]
for app in modules_define:
        application.register_blueprint(app)