from flask import Flask

app = Flask(__name__)
app.config.from_object('config_b3')

from backend3 import views