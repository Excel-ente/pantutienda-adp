from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def generar_token_oauth():
    creds = None
    CLIENT_SECRET_FILE = 'client_secret.json'

    # Revisar si ya existe un token
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # Generar nuevas credenciales si no son válidas
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Guardar el nuevo token
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds

# Ejecutar la función para generar el token
generar_token_oauth()
