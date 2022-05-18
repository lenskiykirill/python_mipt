from flask import Flask
app = Flask(__name__)

from app import db_logic
db_logic.init()

from app import routes
