def create_app():
    try:
        print("🚀 create_app() started")

        from flask import Flask
        from extensions import db, login_manager
        from models import User
        from models import TravelLog
        from flask_login import current_user, login_user, logout_user, login_required
        from flask import render_template, redirect, url_for, request, flash, jsonify, abort
        from werkzeug.security import check_password_hash, generate_password_hash
        from datetime import datetime

        app = Flask(__name__)
        print("✅ Flask app initialized")

        app.config["SECRET_KEY"] = "013eef93b518082e667c7578a0220857973d3374123bd5043ceb8a3334c160d5"
        app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+pg8000://postgres:CarbonCRED@34.59.6.90:5432/carbon_credits"

        db.init_app(app)
        login_manager.init_app(app)
        print("✅ Extensions initialized")

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

        @app.route("/")
        def home():
            return redirect(url_for('login'))

        @app.route('/login', methods=['GET', 'POST'])
        def login():
            try:
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

            except Exception as e:
                print(f"❌ Error in /login route: {e}")
                return "❌ Server error: " + str(e), 500

        @app.route('/logout')
        @login_required
        def logout():
            logout_user() 
            flash('You have been logged out', 'success')
            return redirect(url_for('login'))

        @app.route('/register', methods=['GET', 'POST'])
        def register():
            if request.method == 'POST':
                username = request.form.get('username')
                password = request.form.get('password')
                role = request.form.get('role')  # 'employee' or 'employer'
                
                # Validate input
                if not all([username, password, role]):
                    flash('All fields are required', 'error')
                    return redirect(url_for('register'))
                
                # Check if username exists
                if User.query.filter_by(username=username).first():
                    flash('Username already exists', 'error')
                    return redirect(url_for('register'))
                
                # Create new user
                new_user = User(
                    username=username,
                    password=generate_password_hash(password),  # Hashed!
                    role=role,
                    saved_miles=0 if role == 'employee' else None
                )
                
                db.session.add(new_user)
                db.session.commit()
                
                flash('Registration successful! Please login', 'success')
                return redirect(url_for('login'))
            
            return render_template('auth/register.html')

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
                return render_template("employer/manage_employees.html", employees=employees)
            except Exception as e:
                flash("Error: {}".format(e), "error")
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
        
        def calculate_credits(mode, miles):
            CREDIT_RATES = {
                'car': 0,
                'carpool': 0.5,
                'bus': 0.7,
                'bike': 1.0,
                'wfh': 1.5
            }
            return CREDIT_RATES.get(mode, 0) * miles

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

        @app.route('/debug-users')
        def debug_users():
            users = User.query.all()
            return jsonify([{"id": u.id, "username": u.username, "role": u.role} for u in users])


        with app.app_context():
            db.create_all()
            print("✅ Tables created")

        return app

    except Exception as e:
        print(f"❌ Error in create_app: {e}")
        raise e
