from flask import Flask
import database

app = Flask(__name__)
app.config.from_object('config')
db = database.db_init()

from app import views
