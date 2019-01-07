from flask import Flask
from flasgger import Swagger
from . import storage

app = Flask(__name__)

swagger = Swagger(app)

storage.create_tables()