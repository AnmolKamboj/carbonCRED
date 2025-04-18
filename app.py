from flask import Flask, render_template, redirect, url_for, request, flash, abort
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import jsonify
import os
from google.cloud.sql.connector import Connector, IPTypes
import sqlalchemy

# Initialize Flask app first
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-fallback-key")

# Database configuration - REPLACE LINES 14-52 WITH THIS
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

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+pg8000://"
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "creator": init_connection(),
    "pool_recycle": 300  # Recycle connections every 5 minutes
}

db = SQLAlchemy(app)  # Initialize normally without engine parameter

# Mock database
users = {
    "employee1": {"password": "pass123", "role": "employee", "saved_miles": 750},
    "employer1": {"password": "pass123", "role": "employer"}
}

# Flask-Login setup
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Credit calculation rates
CREDIT_RATES = {
    'car': 0,
    'carpool': 0.5,
    'bus': 0.7,
    'bike': 1.0,
    'wfh': 1.5
}

def calculate_credits(mode, miles):
    return CREDIT_RATES.get(mode, 0) * miles

class TravelLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    date = db.Column(db.Date)
    mode = db.Column(db.String(64))
    miles = db.Column(db.Float)
    credits_earned = db.Column(db.Float)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(64), nullable=False)
    saved_miles = db.Column(db.Float, default=0)

@login_manager.user_loader
def load_user(user_id):
    if user_id not in users:
        return None
    user = User()
    user.id = user_id
    user.role = users[user_id]["role"]
    return user

# Routes
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in users and password == users[username]["password"]:
            user = User()
            user.id = username
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid username or password', 'error')
    return render_template('auth/login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'employee':
        return redirect(url_for('employee_dashboard'))
    return redirect(url_for('employer_dashboard'))

@app.route('/employee/dashboard')
@login_required
def employee_dashboard():
    try:
        logs = TravelLog.query.filter_by(employee_id=current_user.id).all()
        total_credits = sum(log.credits_earned for log in logs)
        return render_template("employee_dashboard.html", logs=logs, total_credits=total_credits)
    except Exception as e:
        flash("Error: {}".format(e), "error")
        return redirect(url_for("home"))

@app.route('/employer/dashboard')
@login_required
def employer_dashboard():
    if current_user.role != 'employer':
        abort(403)
    return render_template('employer/dashboard.html')

@app.route('/employer/manage-employees')
@login_required
def manage_employees():
    try:
        employees = User.query.filter_by(role="employee").all()
        return render_template("manage_employees.html", employees=employees)
    except Exception as e:
        flash("Error: {}".format(e), "error")
        return redirect(url_for("home"))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))

@app.route('/employer/marketplace')
@login_required
def marketplace():
    if current_user.role != 'employer':
        abort(403)
    
    credits_for_sale = [
        {"seller": "EcoCorp", "credits": 1500, "price_per_credit": 2.50},
        {"seller": "GreenTech", "credits": 800, "price_per_credit": 3.00}
    ]
    
    return render_template('employer/marketplace.html', credits_for_sale=credits_for_sale)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        
        if username in users:
            flash('Username already exists', 'error')
        else:
            users[username] = {
                "password": password,  
                "role": role,
                "saved_miles": 0 if role == 'employee' else None
            }
            flash('Registration successful! Please login', 'success')
            return redirect(url_for('login'))
    
    return render_template('auth/register.html')

@app.route('/employee/travel-log', methods=['GET', 'POST'])
@login_required
def travel_log():
    if current_user.role != 'employee':
        abort(403)
    
    if request.method == 'POST':
        date = request.form.get('date')
        mode = request.form.get('mode')
        miles = float(request.form.get('miles'))
        
        flash('Travel logged successfully!', 'success')
        return redirect(url_for('travel_log'))
    
    return render_template('employee/travel_log.html')

@app.route('/log-trip', methods=['POST'])
@login_required 
def log_trip():
    data = request.get_json()
    miles = float(data['miles'])
    mode = data['mode']
    
    credits = calculate_credits(mode, miles)
    
    new_log = TravelLog(
        employee_id=current_user.id,
        date=datetime.utcnow().date(),
        mode=mode,
        miles=miles,
        credits_earned=credits
    )
    db.session.add(new_log)
    db.session.commit()
    
    return jsonify({"credits": credits})

if __name__ == '__main__':
    app.run(debug=True)