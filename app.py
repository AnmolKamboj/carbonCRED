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

        app.config["SECRET_KEY"] = "your-hardcoded-dev-key"
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

        with app.app_context():
            db.create_all()
            print("✅ Tables created")

        return app

    except Exception as e:
        print(f"❌ Error in create_app: {e}")
        raise
