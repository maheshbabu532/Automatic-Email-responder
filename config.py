import os

# Choose your database type
DATABASE_URI = "mysql+pymysql://flask_user:1234@localhost/flask_app_db"  # For MySQL 
# DATABASE_URI = "postgresql://user:password@localhost/dbname"  # For PostgreSQL
# DATABASE_URI = "mysql://user:password@localhost/dbname"  # For MySQL

class Config:
    SQLALCHEMY_DATABASE_URI = DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False

EMAIL_HOST = "imap.gmail.com"  # IMAP for reading emails
SMTP_HOST = "smtp.gmail.com"  # SMTP for sending emails
EMAIL_PORT = 993
SMTP_PORT = 587
EMAIL_ADDRESS = "maheshnani.maddigunta@gmail.com"
EMAIL_PASSWORD = "app password"  # Use App Password if using Gmail
