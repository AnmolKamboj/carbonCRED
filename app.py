from flask import Flask, render_template, redirect, url_for, request, flash, abort
#from datetime import datetime
#from flask import jsonify
import os
#from werkzeug.security import generate_password_hash
from extensions import (
    db, 
    login_manager, 
    init_connection,
    current_user,
    login_user,
    logout_user,
    login_required
)
#from models import User, TravelLog
#from werkzeug.security import check_password_hash

def create_app():

    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-fallback-key")
    
    # Database configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+pg8000://postgres:CarbonCred%40123@34.59.6.90:5432/carbon_credits"

    # Initialize extensions
    db.init_app(app)
    #login_manager.init_app(app)

    # Mock database (could move to a separate file)
    users = {
        "employee1": {"password": "pass123", "role": "employee", "saved_miles": 750},
        "employer1": {"password": "pass123", "role": "employer"}
    }
    
    # Credit calculation rates (could move to config)
    CREDIT_RATES = {
        'car': 0,
        'carpool': 0.5,
        'bus': 0.7,
        'bike': 1.0,
        'wfh': 1.5
    }
    
    # Register blueprints or routes
    #register_routes(app, users, CREDIT_RATES)

    #with app.app_context():
        #db.create_all()  # Initialize database tables
    @app.route("/")
    def hello():
       return render_template("index.html")
    
    return app


    