from flask import Flask
from dotenv import load_dotenv
#from flask_migrate import Migrate
#from flask_sqlalchemy import SQLAlchemy
#from flask_cors import CORS

import os
import sys

load_dotenv()


app = Flask(__name__)

#CORS(app)
#app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("CADENA_CONEXION_BASE_DE_DATOS")
#SQLAlchemy(app)


@app.route("/ping")
def ping():
    return "pong"