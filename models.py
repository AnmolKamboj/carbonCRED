from extensions import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'   # <<< ADD THIS LINE

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(64), nullable=False)
    saved_miles = db.Column(db.Float, default=0)
    employer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    home_address = db.Column(db.String(255), nullable=True)
    work_address = db.Column(db.String(255), nullable=True)
    approved = db.Column(db.Boolean, default=False)

class TravelLog(db.Model):
    __tablename__ = 'travel_logs'  # (optional but cleaner)

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date = db.Column(db.Date)
    mode = db.Column(db.String(64))
    miles = db.Column(db.Float)
    credits_earned = db.Column(db.Float)
