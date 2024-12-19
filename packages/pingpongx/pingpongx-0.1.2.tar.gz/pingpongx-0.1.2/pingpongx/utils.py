from google.cloud import firestore, secretmanager
import json
import requests
import os
import uuid
import re

ONESIGNAL_APP_ID = os.getenv('ONESIGNAL_APP_ID', "")
PROJECT_ID = os.getenv('PROJECT_ID')
ENV = os.environ.get("ENV")


def generate_device_token():
    try:
        url = "https://onesignal.com/api/v1/players"

        payload = {
            "device_type": 5,
            "language": "en",
            "timezone": "-28800",
            "game_version": "1.1.1",
            "device_model": "iPhone5,1",
            "device_os": "15.1.1",
            "session_count": 600,
            "tags": {
                "first_name": "Jon",
                "last_name": "Smith",
                "level": "99",
                "amount_spent": "6000",
                "account_type": "VIP"
            },
            "amount_spent": "100.99",
            "playtime": 600,
            "notification_types": 1,
            "lat": 37.563,
            "long": 122.3255,
            "country": "US",
            "timezone_id": "Asia/Kolkata",
            "app_id": ONESIGNAL_APP_ID
        }
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)
        return response.json()
    except Exception as e:
        print(e)


def generate_notification_id():
    return str(uuid.uuid4())


def validate_email(email):
    """Validates an email address using a regular expression."""
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None


def validate_phone_number(phone_number):
    """Validates a phone number."""
    phone_regex = r"^\+(?:[0-9] ?){6,14}[0-9]$"
    return re.match(phone_regex, phone_number) is not None


def sanitize_topic_name(topic_name):
    # Replace "@" with "-" to make the topic name valid
    sanitized_topic_name = topic_name.replace('@', '-')
    return sanitized_topic_name


def get_db_via_firebase_credentials():
    try:
        print("environment: ", ENV)
        if ENV == "dev":
            return firestore.Client.from_service_account_json("firebase_credentials.json")
        elif ENV == "local":
            client = secretmanager.SecretManagerServiceClient()
            secret_name = f"projects/424159745652/secrets/FIREBASE_CREDENTIALS/versions/2"
            response = client.access_secret_version(name=secret_name)
            credentials = response.payload.data.decode("UTF-8")
            return firestore.Client.from_service_account_info(json.loads(credentials))
        else:
            return firestore.Client()
    except Exception as e:
        print(f"Error getting firebase credentials: {e}")
        return None
