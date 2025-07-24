from flask import Flask
from dotenv import load_dotenv

from utils.db import db
from flask_cors import CORS

import os
import sys

load_dotenv()


app = Flask(__name__)

CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_CONNECTION_STRING")


@app.route("/ping")
def ping():
    return "pong"