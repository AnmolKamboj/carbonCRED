from flask import Flask
from extensions import db, login_manager

def create_app():
    from models import User  # avoid circular import
    from flask_login import current_user, login_user, logout_user, login_required
    from flask import render_template, redirect, url_for, request, flash, jsonify, abort
    from werkzeug.security import check_password_hash, generate_password_hash
    from datetime import datetime

    app = Flask(__name__)
    app.config["SECRET_KEY"] = "your-hardcoded-dev-key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"  # or your PostgreSQL URI

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            role = request.form.get("role")

            if User.query.filter_by(username=username).first():
                flash("Username already exists", "error")
                return redirect(url_for("register"))

            user = User(username=username, password=generate_password_hash(password), role=role)
            db.session.add(user)
            db.session.commit()

            flash("Registered successfully!", "success")
            return redirect(url_for("login"))
        return "Register Page Placeholder"

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                return "Logged in!"
            flash("Invalid login")
        return "Login Page Placeholder"

    with app.app_context():
        db.create_all()

    return app
