def create_app():
    try:
        print("🚀 create_app() started")

        from flask import Flask
        from extensions import db, login_manager
        from models import User
        from flask_login import current_user, login_user, logout_user, login_required
        from flask import render_template, redirect, url_for, request, flash, jsonify, abort
        from werkzeug.security import check_password_hash, generate_password_hash
        from datetime import datetime

        app = Flask(__name__)
        print("✅ Flask app initialized")

        app.config["SECRET_KEY"] = "013eef93b518082e667c7578a0220857973d3374123bd5043ceb8a3334c160d5"
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"

        db.init_app(app)
        login_manager.init_app(app)
        print("✅ Extensions initialized")

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

        @app.route("/")
        def index():
            return "✅ App running!"

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

        '''@app.route('/employee/dashboard')
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
                return redirect(url_for("home"))'''

        @app.route('/employer/dashboard')
        @login_required
        def employer_dashboard():
            if current_user.role != 'employer':
                abort(403)
            return render_template('employer/dashboard.html')

        with app.app_context():
            db.create_all()
            print("✅ Tables created")

        return app

    except Exception as e:
        print(f"❌ Error in create_app: {e}")
        raise
