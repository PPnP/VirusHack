from flask import Flask
from flask_script import Manager


app = Flask(__name__, template_folder='./templates', static_folder='./static')
app.config.from_object('config')

manager = Manager(app)
