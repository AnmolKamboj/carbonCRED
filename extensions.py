# extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from google.cloud.sql.connector import Connector, IPTypes
import os

db = SQLAlchemy()
login_manager = LoginManager()

# Export all needed Flask-Login components
__all__ = ['db', 'login_manager', 'current_user', 'login_user', 'logout_user', 'login_required']

def init_connection():
    connector = Connector()
    def getconn():
        return connector.connect(
            os.environ["INSTANCE_CONNECTION_NAME"],
            "pg8000",
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASS"],
            db=os.environ["DB_NAME"],
            ip_type=IPTypes.PUBLIC
        )
    return getconn