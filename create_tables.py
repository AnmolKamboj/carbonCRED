from app import create_app
from extensions import db, init_connection
from models import User, TravelLog
from werkzeug.security import generate_password_hash
from datetime import datetime
import sys

app = create_app()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
'''app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
            "creator": init_connection(),
            "pool_recycle": 300
    }'''

with app.app_context():
    confirm = input("⚠️  Are you sure you want to DROP ALL TABLES? (yes/no): ")
    if confirm.lower() != "yes":
        print("❌ Aborted.")
        sys.exit()

    db.drop_all()
    db.create_all()
    print("✔ Tables dropped and recreated")

    # Create users with approval flow
    employer = User(
        username="employer1",
        password=generate_password_hash("pass123"),
        role="employer",
        approved=False
    )
    employee = User(
        username="employee1",
        password=generate_password_hash("pass123"),
        role="employee",
        saved_miles=300,
        approved=False,
        employer=employer
    )
    bank = User(
        username="bank1",
        password=generate_password_hash("pass123"),
        role="bank",
        approved=True
    )

    db.session.add_all([employee, employer, bank])
    db.session.commit()

    logs = [
        TravelLog(employee_id=employee.id, date=datetime(2024, 4, 1), mode="carpool", miles=10, credits_earned=5),
        TravelLog(employee_id=employee.id, date=datetime(2024, 4, 2), mode="bike", miles=5, credits_earned=5),
        TravelLog(employee_id=employee.id, date=datetime(2024, 4, 3), mode="wfh", miles=0, credits_earned=0)
    ]
    db.session.add_all(logs)
    db.session.commit()
    print("✔ Mock data inserted")
