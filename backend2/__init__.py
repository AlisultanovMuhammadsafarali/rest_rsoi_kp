from flask import Flask

app = Flask(__name__)
app.config.from_object('config_b2')

from backend2 import views