from flask import Flask
from extensions import db, login_manager
from models import User, TravelLog

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "013eef93b518082e667c7578a0220857973d3374123bd5043ceb8a3334c160d5"
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+pg8000://postgres:CarbonCred%40123@34.59.6.90:5432/carbon_credits"  # or your real DB

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/')
    def index():
        return "✅ App is working with models + extensions!"

    with app.app_context():
        db.create_all()

    return app


'''def register_routes(app, db, login_manager, User, TravelLog):
    from extensions import current_user, login_user, logout_user, login_required

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

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/')
    def home():
        return redirect(url_for('login'))
    
    @app.route('/test')
    def test():
        return "✅ Flask is alive"
    
    @app.route('/debug-routes')
    def debug_routes():
        return jsonify([str(rule) for rule in app.url_map.iter_rules()])



    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))

            flash('Invalid username or password', 'error')
        return render_template('auth/login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('You have been logged out', 'success')
        return redirect(url_for('login'))

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
            return render_template(
                "employee/dashboard.html",
                logs=logs,
                total_credits=total_credits,
                saved_miles=current_user.saved_miles
            )
        except Exception as e:
            flash(f"Error: {e}", "error")
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
            return render_template("employer/manage_employees.html", employees=employees)
        except Exception as e:
            flash(f"Error: {e}", "error")
            return redirect(url_for("home"))

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

            if not all([username, password, role]):
                flash('All fields are required', 'error')
                return redirect(url_for('register'))

            if User.query.filter_by(username=username).first():
                flash('Username already exists', 'error')
                return redirect(url_for('register'))

            new_user = User(
                username=username,
                password=generate_password_hash(password),
                role=role,
                saved_miles=0 if role == 'employee' else None
            )
            db.session.add(new_user)
            db.session.commit()

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

    @app.context_processor
    def inject_user():
        return dict(user=current_user)'''
