from flask import Flask, render_template, redirect, url_for, request, flash, abort
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.secret_key = 'dev'  # Required for flash messages and sessions

# Mock database
users = {
    "employee1": {"password": "pass123", "role": "employee", "saved_miles": 750},
    "employer1": {"password": "pass123", "role": "employer"}
}

# Flask-Login setup
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin):
    pass

def get_employees():
    """Mock data - replace with real database query"""
    return [
        {"username": "employee1", "saved_miles": 750},
        {"username": "employee2", "saved_miles": 420}
    ]

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
    """Route that redirects to role-specific dashboard"""
    if current_user.role == 'employee':
        return redirect(url_for('employee_dashboard'))
    return redirect(url_for('employer_dashboard'))

@app.route('/employee/dashboard')
@login_required
def employee_dashboard():
    if current_user.role != 'employee':
        abort(403)
    return render_template('employee/dashboard.html',
        saved_miles=750,  # Mock data
        earned_credits=45,
        recent_logs=[]
    )

@app.route('/employer/dashboard')
@login_required
def employer_dashboard():
    if current_user.role != 'employer':
        abort(403)
    return render_template('employer/dashboard.html')

@app.route('/employer/manage-employees')
@login_required
def manage_employees():
    if current_user.role != 'employer':
        abort(403)
    return render_template('employer/manage_employees.html',
        employees=get_employees()  # You'll need to implement this function
    )

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
    
    # Mock data - replace with real database queries
    credits_for_sale = [
        {"seller": "EcoCorp", "credits": 1500, "price_per_credit": 2.50},
        {"seller": "GreenTech", "credits": 800, "price_per_credit": 3.00}
    ]
    
    return render_template('employer/marketplace.html', 
                         credits_for_sale=credits_for_sale)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')  # 'employee' or 'employer'
        
        if username in users:
            flash('Username already exists', 'error')
        else:
            users[username] = {
                "password": password,  # In production, hash this!
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
        abort(403)  # Only employees can access
    
    if request.method == 'POST':
        # Process form submission
        date = request.form.get('date')
        mode = request.form.get('mode')
        miles = float(request.form.get('miles'))
        
        # Add to database (or mock storage)
        flash('Travel logged successfully!', 'success')
        return redirect(url_for('travel_log'))
    
    return render_template('employee/travel_log.html')

# ... (keep other routes the same as before)

if __name__ == '__main__':
    app.run(debug=True)