from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from extensions import db

# ✅ Initialize Flask App
app = Flask(__name__)
app.config.from_object(Config)  # ✅ Use MySQL or SQLite from config

# ✅ Initialize Database & Migration
db.init_app(app)
migrate = Migrate(app,db)

# ✅ Import models after initializing db
from models import Email
from email_handler import fetch_emails, send_auto_response

# ✅ Routes
@app.route("/")
def index():
    emails = Email.query.order_by(Email.received_at.desc()).all()
    return render_template("index.html", emails=emails)

@app.route("/email/<int:email_id>")
def email_details(email_id):
    email = Email.query.get_or_404(email_id)
    return render_template("email_details.html", email=email)

@app.route("/process-emails")
def process_emails():
    fetch_emails()
    for email in Email.query.filter_by(response_sent=False).all():
        send_auto_response(email.sender, email.category)
        email.response_sent = True
        db.session.commit()
    return "Emails processed successfully!"
@app.route('/emails')
def view_emails():
    emails = Email.query.order_by(Email.id.desc()).all()
    return render_template('emails.html', emails=emails)

# ✅ Run the Flask App
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
