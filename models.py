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
    total_credits = db.Column(db.Integer, default=10)

class TravelLog(db.Model):
    __tablename__ = 'travel_logs'  # (optional but cleaner)

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date = db.Column(db.Date)
    mode = db.Column(db.String(64))
    miles = db.Column(db.Float)
    credits_earned = db.Column(db.Float)

class MarketplaceListing(db.Model):
    __tablename__ = 'marketplace_listings'
    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    credits = db.Column(db.Integer, nullable=False)
    price_per_credit = db.Column(db.Float, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.now())

    seller = db.relationship('User', foreign_keys=[seller_id], backref='listings_sold')
    buyer = db.relationship('User', foreign_keys=[buyer_id], backref='listings_bought')