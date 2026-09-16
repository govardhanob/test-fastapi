import firebase_admin
from firebase_admin import credentials, firestore


cred = credentials.Certificate("app/test-5f434-firebase-adminsdk-fbsvc-911d3ec5b0.json")

firebase_admin.initialize_app(cred)

db = firestore.client()