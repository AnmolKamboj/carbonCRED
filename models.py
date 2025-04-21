# models.py
from extensions import db
from flask_login import UserMixin

class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    employer_id = db.Column(db.Integer, db.ForeignKey('employers.id'))
    # Add relationship if needed
    # employer = db.relationship('Employer', backref='employees')

class TravelLog(db.Model):
    __tablename__ = 'travel_logs'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    date = db.Column(db.Date)
    mode = db.Column(db.String(50))
    miles = db.Column(db.Float)
    credits_earned = db.Column(db.Float)
    # Add relationship
    # employee = db.relationship('Employee', backref='travel_logs')

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(64), nullable=False)
    saved_miles = db.Column(db.Float, default=0)