from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_user, logout_user, login_required

# ✅ Don't do anything risky here — just instantiate
db = SQLAlchemy()
login_manager = LoginManager()

__all__ = [
    "db", "login_manager", "current_user",
    "login_user", "logout_user", "login_required"
]
