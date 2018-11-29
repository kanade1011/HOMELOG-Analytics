from flask import Flask
from api import register, result_creater, processor

application = Flask(__name__)

modules_define = [register.register, result_creater.api]
for app in modules_define:
        application.register_blueprint(app)