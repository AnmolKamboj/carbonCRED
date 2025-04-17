from app import db
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    employer_id = db.Column(db.Integer, db.ForeignKey('employer.id'))

class TravelLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    date = db.Column(db.Date)
    mode = db.Column(db.String(50))  # 'car', 'bus', 'carpool', 'bike', 'wfh'
    miles = db.Column(db.Float)
    credits_earned = db.Column(db.Float)  # Calculated field