from flask import Flask
import api.register as serve

application = Flask(__name__)

modules_define = [serve.register]
for app in modules_define:
        application.register_blueprint(app)