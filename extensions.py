from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# ✅ Flask extensions
db = SQLAlchemy()
login_manager = LoginManager()

# ✅ Cloud SQL Proxy connector
from google.cloud.sql.connector import Connector, IPTypes
import os

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
