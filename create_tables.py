from app import create_app
from extensions import db
from models import User, TravelLog
from werkzeug.security import generate_password_hash
from datetime import datetime

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()
    print("✔ Tables dropped and recreated")

    employee = User(
        username="employee1",
        password=generate_password_hash("pass123"),
        role="employee",
        saved_miles=300
    )
    employer = User(
        username="employer1",
        password=generate_password_hash("pass123"),
        role="employer"
    )
    db.session.add_all([employee, employer])
    db.session.commit()

    logs = [
        TravelLog(employee_id=employee.id, date=datetime(2024, 4, 1), mode="carpool", miles=10, credits_earned=5),
        TravelLog(employee_id=employee.id, date=datetime(2024, 4, 2), mode="bike", miles=5, credits_earned=5),
        TravelLog(employee_id=employee.id, date=datetime(2024, 4, 3), mode="wfh", miles=0, credits_earned=0)
    ]
    db.session.add_all(logs)
    db.session.commit()
    print("✔ Mock data inserted")
