from extensions import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(64), nullable=False)
    saved_miles = db.Column(db.Float, default=0)
    approved = db.Column(db.Boolean, default=False)
    employer_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)  # if employee
    employees = db.relationship("User", backref=db.backref("employer", remote_side=[id]), lazy=True)

class TravelLog(db.Model):
    __tablename__ = "travel_logs"
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    date = db.Column(db.Date)
    mode = db.Column(db.String(50))
    miles = db.Column(db.Float)
    credits_earned = db.Column(db.Float)
