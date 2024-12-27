from kafka import KafkaConsumer
import json
import smtplib
from email.mime.text import MIMEText
import os

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka-local.drowning-detector.svc.cluster.local:9092")

# Kafka Consumer Configuration
consumer = KafkaConsumer(
    'drowning-alerts',
    bootstrap_servers = KAFKA_BROKER,
    group_id = "email-alert-service",
    auto_offset_reset = 'earliest' # start reading from the beginning if no offset
)

# Email Configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = 'SMTP_USERNAME'
SMTP_PASSWORD = 'SMTP_PASSWORD'

def send_email(subject, body, to_email):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SMTP_USERNAME
    msg['To'] = to_email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SMTP_USERNAME, to_email, msg.as_string())
            print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Consume and Send Alerts
print("Listening for drowning alerts...")
for message in consumer:
    try:
        alert_data = message.value.decode('utf-8') # Deserialize message
        print(f"Received Alert: {alert_data}")

        # Customize email content
        alert = f"Drowning Alert:\n\n{alert_data}"
        subject = "Emergency Alert: Drowning Detected!"
        to_email = "ngophong1019@gmail.com"

        # Send the email
        send_email(subject, alert, to_email)

    except Exception as e:
        print(f"Error processing message: {e}")