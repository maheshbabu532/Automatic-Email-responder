import smtplib
from email.mime.text import MIMEText
from config import SMTP_HOST, SMTP_PORT, EMAIL_ADDRESS, EMAIL_PASSWORD

def send_auto_response(to_email, category):
    responses = {
        "Urgent": "We have received your urgent request. Our team is looking into it immediately.",
        "General": "Thank you for reaching out. We will get back to you within 24 hours.",
        "Spam": "This email appears to be spam and will not be processed."
    }
    message = MIMEText(responses.get(category, "We received your email."))
    message["Subject"] = "Re: Your Support Request"
    message["From"] = EMAIL_ADDRESS
    message["To"] = to_email

    server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    server.sendmail(EMAIL_ADDRESS, to_email, message.as_string())
    server.quit()
