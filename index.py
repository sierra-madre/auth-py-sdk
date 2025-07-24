from app import  app
from utils.db import db
import os

from dotenv import load_dotenv
load_dotenv()

"""
from flask_migrate import Migrate
migrate = Migrate(app, db)
"""

db.init_app(app)


with app.app_context():
    db.create_all()





if __name__ == "__main__":
    host = os.getenv('HOST')
    if host is None:
        host = '127.0.0.1'

    app.run(debug=True, host=host,port=5001)