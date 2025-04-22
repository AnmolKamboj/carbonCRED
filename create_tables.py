from app import create_app
from extensions import db
from models import User, TravelLog
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db.drop_all()   # ✅ Important for development: drop old tables
    db.create_all() # ✅ Recreate tables freshly
    print("✔ Tables dropped and created successfully!")

    # Then insert your mock users
    if not User.query.filter_by(username="employee1").first():
        user1 = User(
            username="employee1",
            password=generate_password_hash("pass123"),
            role="employee",
            saved_miles=750
        )
        db.session.add(user1)

    if not User.query.filter_by(username="employer1").first():
        user2 = User(
            username="employer1",
            password=generate_password_hash("pass123"),
            role="employer"
        )
        db.session.add(user2)

    db.session.commit()
    print("✔ Mock users created successfully!")
