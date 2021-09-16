from flask import Flask
from config import Config
from app.connection import Connection

app = Flask(__name__)
app.config.from_object(Config)
con = Connection()

from app import routes
