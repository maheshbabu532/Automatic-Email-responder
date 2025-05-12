from datetime import datetime
from extensions import db  # ✅ Import after db is initialized in app.py

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"

class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(255), unique=True)
    sender = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # Urgent, General, Spam
    received_at = db.Column(db.DateTime, default=datetime.utcnow)
    response_sent = db.Column(db.Boolean, default=False)
    response_message = db.Column(db.Text, nullable=True) 
    def __repr__(self):
        return f"<Email {self.subject} - {self.category}>"
