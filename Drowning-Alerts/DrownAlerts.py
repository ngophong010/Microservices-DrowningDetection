from kafka import KafkaConsumer
from kafka.errors import KafkaError
from kafka.admin import KafkaAdminClient, NewTopic
from datetime import datetime
import json
import smtplib
from email.mime.text import MIMEText
import os
import logging

logging.basicConfig(level=logging.DEBUG)

# Kafka configurations
KAFKA_TOPIC = "drowning-alerts"
BOOTSTRAP_SERVER = os.getenv("KAFKA_BROKER", "kafka-local.drowning-detector.svc.cluster.local:9092")

# Kafka Consumer Configuration
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers = BOOTSTRAP_SERVER,
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    group_id = "drowning-alert-service",
    auto_offset_reset = 'earliest',
    security_protocol="SASL_PLAINTEXT",
    sasl_mechanism="SCRAM-SHA-256",
    sasl_plain_username="user1",
    sasl_plain_password="9WO6HhtXKB",

    # Add these parameters for better debugging
    enable_auto_commit=True,
    session_timeout_ms=6000,
    heartbeat_interval_ms=3000
)

admin_client = KafkaAdminClient(
    bootstrap_servers=BOOTSTRAP_SERVER,
    security_protocol="SASL_PLAINTEXT",
    sasl_mechanism="SCRAM-SHA-256",
    sasl_plain_username="user1",
    sasl_plain_password="9WO6HhtXKB"
)

# List all topics
topics = admin_client.list_topics()
print(f"Available topics: {topics}")

# Add connection verification
try:
    # Check if consumer is connected
    topics = consumer.topics()
    print(f"Available topics: {topics}")
    partitions = consumer.partitions_for_topic(KAFKA_TOPIC)
    print(f"Partitions for {KAFKA_TOPIC}: {partitions}")
    
    # Check consumer group assignment
    print(f"Assignment: {consumer.assignment()}")
except KafkaError as e:
    print(f"Kafka connection error: {e}")

# Email Configuration
# Mailtrap Email Configuration
SMTP_SERVER = 'live.smtp.mailtrap.io'
SMTP_PORT = 587
SMTP_USERNAME = 'api'  # Replace with your actual Mailtrap username
SMTP_PASSWORD = '6571292c2bf2bb5a83bfb13a0cbec30d'  # Replace with your actual Mailtrap password

SENDER_EMAIL = "hello@demomailtrap.com"
RECEIVER_EMAIL = "ngophong1019@gmail.com"

def send_email(subject, body, to_email):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = to_email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
            print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Consume and Send Alerts
print("Listening for drowning alerts...")
for message in consumer:
    try:
        alert_data = message.value # Deserialize message
        print(f"Received Alert: {alert_data}")

        # Customize email content
        alert = f"Drowning Alert:\n\n{json.dumps(alert_data, indent=2)}"  # Format dict for readability
        subject = "Emergency Alert: Drowning Detected!"

        # Send the email
        send_email(subject, alert, RECEIVER_EMAIL)

    except Exception as e:
        print(f"Error processing message: {e}")
