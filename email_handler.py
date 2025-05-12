import imaplib
import email
from config import EMAIL_HOST, EMAIL_PORT, EMAIL_ADDRESS, EMAIL_PASSWORD
from models import db, Email
import smtplib
from email.mime.text import MIMEText
from config import SMTP_HOST, SMTP_PORT, EMAIL_ADDRESS, EMAIL_PASSWORD
from classifier import classify_email

def fetch_emails():
    mail = imaplib.IMAP4_SSL(EMAIL_HOST, EMAIL_PORT)
    mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    mail.select("inbox")

    result, data = mail.search(None, "UNSEEN")  # Fetch unread emails
    email_ids = data[0].split()

    for e_id in email_ids:
        result, msg_data = mail.fetch(e_id, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        message_id = msg.get("Message-ID")

        # Skip if already processed
        existing = Email.query.filter_by(uid=message_id).first()
        if existing:
            continue  # Don't process or respond again

        sender = msg["From"]
        subject = msg["Subject"]
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
               if part.get_content_type() == "text/plain":
                   payload = part.get_payload(decode=True)
                   try:
                       body = payload.decode('utf-8')
                   except UnicodeDecodeError:
        # fallback decoding
                            try:
                                body = payload.decode('latin-1')
                            except:
                                body = payload.decode('utf-8', errors='ignore')  # fallback to ignore errors


        category = classify_email(subject, body)  # Classify using NLP
        response_message=send_auto_response(sender, category)
        new_email = Email(sender=sender, subject=subject, body=body, category=category , response_message=response_message)
        db.session.add(new_email)
        db.session.commit()

        mail.store(e_id, '+FLAGS', '\\Seen')

    mail.logout()
def send_auto_response(to_email, category):
    responses = {
        "Urgent": "We have received your urgent request. Our team is looking into it immediately.",
        "General": "Thank you for reaching out. We will get back to you within 24 hours.",
        "Spam": "This email appears to be spam and will not be processed."
    }
    response = responses.get(category, "We received your email.")

    message = MIMEText(responses.get(category, "We received your email."))
    message["Subject"] = "Re: Your Support Request"
    message["From"] = EMAIL_ADDRESS
    message["To"] = to_email
    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, to_email, message.as_string())
        server.quit()
        return response
    except Exception as e:
        print("Error sending email:", str(e))
        return None