def create_app():
    try:
        print("🚀 create_app() started")

        from flask import Flask
        from extensions import db, login_manager, init_connection
        from models import User
        from models import TravelLog
        from flask_login import current_user, login_user, logout_user, login_required
        from flask import render_template, redirect, url_for, request, flash, jsonify, abort
        from werkzeug.security import check_password_hash, generate_password_hash
        from datetime import datetime
        from approval_routes import approval


        app = Flask(__name__)
        print("✅ Flask app initialized")

        app.config["SECRET_KEY"] = "013eef93b518082e667c7578a0220857973d3374123bd5043ceb8a3334c160d5"
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
        '''app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
                    "creator": init_connection(),
                    "pool_recycle": 300
            }'''


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
                        if not user.approved:
                            flash("Account pending approval.", "warning")
                            return redirect(url_for("login"))
                        login_user(user)
                        return redirect(url_for("dashboard"))

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
            from models import User

            # fetch employers to show in dropdown
            employers = User.query.filter_by(role='employer', approved=True).all()

            if request.method == 'POST':
                username = request.form.get('username')
                password = request.form.get('password')
                role = request.form.get('role')
                employer_id = request.form.get('employer_id') 
                print("✅ Registration Form Submitted")
                print(f"Username: {username}, Role: {role}, Employer ID: {employer_id}")

                if not all([username, password, role]):
                    flash('All fields are required', 'error')
                    return redirect(url_for('register'))

                if User.query.filter_by(username=username).first():
                    flash('Username already exists', 'error')
                    return redirect(url_for('register'))

                if role == 'employee' and not employer_id:
                    flash('Employee must select an employer.', 'error')
                    return redirect(url_for('register'))

                new_user = User(
                    username=username,
                    password=generate_password_hash(password),
                    role=role,
                    saved_miles=0 if role == 'employee' else None,
                    approved=False,
                    employer_id=int(employer_id) if role == 'employee' else None
                )

                db.session.add(new_user)
                db.session.commit()

                flash('Registration successful! Please login after approval.', 'success')
                return redirect(url_for('login'))

            # If method is GET, show registration form
            return render_template('auth/register.html', employers=employers)


        @app.route('/dashboard')
        @login_required
        def dashboard():
            if current_user.role == 'employee':
                return redirect(url_for('employee_dashboard'))
            elif current_user.role == 'employer':
                return redirect(url_for('employer_dashboard'))
            elif current_user.role == 'bank':
                return redirect(url_for('approval.pending_employers'))
            else:
                abort(403)  # unknown role


        @app.route('/employee/dashboard')
        @login_required
        def employee_dashboard():
            try:
                logs = TravelLog.query.filter_by(employee_id=current_user.id).all()
                total_credits = sum(log.credits_earned for log in logs)

                return render_template(
                    'employee/dashboard.html',
                    travel_logs=logs,
                    total_credits=total_credits,
                    saved_miles=current_user.saved_miles,
                    home_address=current_user.home_address
                )
            except Exception as e:
                flash("Error: {}".format(e), "error")
                return redirect(url_for('home'))
            
        @app.route('/employee/set-home-address', methods=['POST'])
        @login_required
        def employee_set_home_address():
            if current_user.role != 'employee':
                abort(403)

            home_address = request.form.get('home_address')
            if home_address:
                current_user.home_address = home_address
                db.session.commit()
                flash('Home address saved successfully!', 'success')
            
            return redirect(url_for('employee_dashboard'))
    

        @app.route('/employer/dashboard')
        @login_required
        def employer_dashboard():
            if current_user.role != 'employer':
                abort(403)

            # Fetch employees under this employer
            employees = User.query.filter_by(role='employee', employer_id=current_user.id, approved=True).all()

            # Calculate total credits
            total_credits = 0
            leaderboard = []
            for emp in employees:
                employee_logs = TravelLog.query.filter_by(employee_id=emp.id).all()
                emp_credits = sum(log.credits_earned for log in employee_logs)
                total_credits += emp_credits
                leaderboard.append({'username': emp.username, 'total_credits': emp_credits})

            # Sort leaderboard by highest credits
            leaderboard = sorted(leaderboard, key=lambda x: x['total_credits'], reverse=True)

            return render_template(
                'employer/dashboard.html',
                company_name=current_user.username,
                employee_count=len(employees),
                total_credits=total_credits,
                leaderboard=leaderboard,
                work_address=current_user.work_address
            )


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

        @app.route('/employer/set-work-address', methods=['POST'])
        @login_required
        def employer_set_work_address():
            if current_user.role != 'employer':
                abort(403)
            
            work_address = request.form.get('work_address')
            if work_address:
                current_user.work_address = work_address
                db.session.commit()
                flash('Work address saved successfully!', 'success')
            
            return redirect(url_for('employer_dashboard'))
        
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
        
        @app.route("/fix-bank")
        def fix_bank():
            from extensions import db
            from models import User

            bank = User.query.filter_by(username='bank1').first()
            if bank:
                bank.approved = True
                db.session.commit()
                return "✅ Bank user approved!"
            return "❌ Bank user not found."

        app.register_blueprint(approval)

        with app.app_context():
            db.create_all()
            print("✅ Tables created")

        return app

    except Exception as e:
        print(f"❌ Error in create_app: {e}")
        raise e