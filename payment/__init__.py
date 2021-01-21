from flask import Flask
from flask_api import FlaskAPI

app = FlaskAPI(__name__)
app.config['SECRET_KEY'] = '03736ce872503fad701d34b03d399b06'
app.config['DEBUG'] = 1

from payment import routes
