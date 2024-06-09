import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random

def send_verification_email(email):
    # Generate a random verification code
    verification_code = str(random.randint(100000, 999999))

    # Email content
    sender_email = "vasmoto00@gmail.com"
    receiver_email = email
    subject = "Email Verification"
    body = f"Your verification code is: {verification_code}"

    # Setup the email message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Attach the body to the email
    message.attach(MIMEText(body, "plain"))

    # Send the email using Gmail SMTP server
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, "ggapbfuihcpatjre")
        server.sendmail(sender_email, receiver_email, message.as_string())

    return verification_code

# Example usage
