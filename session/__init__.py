from flask import Flask

app = Flask(__name__)
app.config.from_object('config_s1')

from session import views