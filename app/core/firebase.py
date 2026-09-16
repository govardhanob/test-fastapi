import os
from pathlib import Path

import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials, firestore


load_dotenv()

APP_DIR = Path(__file__).resolve().parents[1]
PROJECT_DIR = APP_DIR.parent
LOCAL_SERVICE_ACCOUNT_PATH = APP_DIR / "test-5f434-firebase-adminsdk-fbsvc-911d3ec5b0.json"
GENERIC_SERVICE_ACCOUNT_PATH = PROJECT_DIR / "firebase-service-account.json"


def get_service_account_path() -> Path | None:
    service_account_path = os.getenv("FIREBASE_SERVICE_ACCOUNT")
    if service_account_path:
        return Path(service_account_path)

    google_credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if google_credentials_path:
        return Path(google_credentials_path)

    for path in (GENERIC_SERVICE_ACCOUNT_PATH, LOCAL_SERVICE_ACCOUNT_PATH):
        if path.exists():
            return path

    return None


def initialize_firebase_app():
    if firebase_admin._apps:
        return firebase_admin.get_app()

    service_account_path = get_service_account_path()
    if service_account_path is not None:
        cred = credentials.Certificate(str(service_account_path))
        return firebase_admin.initialize_app(cred)

    return firebase_admin.initialize_app()


initialize_firebase_app()

db = firestore.client()
