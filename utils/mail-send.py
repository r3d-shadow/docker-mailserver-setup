import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate  
import time
import uuid

# Set up the SMTP connection
smtp_server = "mail.example.com"
smtp_port = 587
smtp_username = "admin@mail.example.com"
smtp_password = "PASSWORD"

# Set up the email parameters
sender = "admin@mail.example.com"
subject = "Hi"
body="Hi"

recipients = ["RANDOM-EMAIL"]

for recipient in recipients:
    print("recipient", recipient)
    # Create the email message
    msg = MIMEText(body)
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject
    msg['Date'] = formatdate(localtime=True)  # Add the 'Date' header
    msg['Message-ID'] = "<" + str(uuid.uuid4()) + "@" + smtp_server + ">"

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender, recipient, msg.as_string())
