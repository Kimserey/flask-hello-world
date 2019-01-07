from flask import Flask
from . import storage

app = Flask(__name__)
storage.create_tables()