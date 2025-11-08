# Firebase Admin initialization
import os
import firebase_admin
from firebase_admin import credentials, auth

def init_firebase():
    project_id = os.getenv("FIREBASE_PROJECT_ID")
    client_email = os.getenv("FIREBASE_CLIENT_EMAIL")
    private_key = os.getenv("FIREBASE_PRIVATE_KEY")
    if not (project_id and client_email and private_key):
        return None

    if not firebase_admin._apps:
        cred = credentials.Certificate({
            "type": "service_account",
            "project_id": project_id,
            "private_key_id": "ignored",
            "private_key": private_key.replace('\\n', '\n'),
            "client_email": client_email,
            "client_id": "ignored",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/" + client_email
        })
        firebase_admin.initialize_app(cred)
    return firebase_admin

def verify_id_token(id_token: str):
    if not id_token:
        return None
    init_firebase()
    try:
        return auth.verify_id_token(id_token)
    except Exception:
        return None