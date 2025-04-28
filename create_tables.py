from app import create_app
from extensions import db, init_connection
from models import User, TravelLog, MarketplaceListing
from werkzeug.security import generate_password_hash
from datetime import datetime
import sys
##from dotenv import load_dotenv
##load_dotenv()

app = create_app()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
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

    # Create employers
    employer1 = User(
        username="employer1",
        password=generate_password_hash("pass123"),
        role="employer",
        approved=True,
        total_credits=0
    )
    employer2 = User(
        username="employer2",
        password=generate_password_hash("pass123"),
        role="employer",
        approved=True,
        total_credits=0
    )
    db.session.add_all([employer1, employer2])
    db.session.commit()

    # Create employees
    employee1 = User(
        username="employee1",
        password=generate_password_hash("pass123"),
        role="employee",
        saved_miles=300,
        approved=True,
        employer_id=employer1.id  # Linked to employer1
    )
    employee2 = User(
        username="employee2",
        password=generate_password_hash("pass123"),
        role="employee",
        saved_miles=250,
        approved=True,
        employer_id=employer2.id  # Linked to employer2
    )
    bank = User(
        username="bank1",
        password=generate_password_hash("pass123"),
        role="bank",
        approved=True
    )

    db.session.add_all([employee1, employee2, bank])
    db.session.commit()

    # Create travel logs for employee1
    logs = [
        TravelLog(employee_id=employee1.id, date=datetime(2024, 4, 1), mode="carpool", miles=10, credits_earned=5),
        TravelLog(employee_id=employee1.id, date=datetime(2024, 4, 2), mode="bike", miles=5, credits_earned=5),
        TravelLog(employee_id=employee1.id, date=datetime(2024, 4, 3), mode="wfh", miles=0, credits_earned=0)
    ]
    db.session.add_all(logs)
    db.session.commit()

    total_earned = db.session.query(db.func.sum(TravelLog.credits_earned)).filter_by(employee_id=employee1.id).scalar() or 0
    employer1.total_credits += total_earned
    
    db.session.commit()

    # Insert Marketplace listings
    listing1 = MarketplaceListing(
        seller_id=employer1.id,
        credits=500,
        price_per_credit=2.5
    )
    listing2 = MarketplaceListing(
        seller_id=employer2.id,
        credits=300,
        price_per_credit=3.0
    )
    db.session.add_all([listing1, listing2])
    db.session.commit()
    print("✔ Mock data inserted")
