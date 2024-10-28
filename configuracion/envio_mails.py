import os
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.template.loader import render_to_string
import environ

# Inicializa django-environ para leer el archivo .env
env = environ.Env()
environ.Env.read_env()  # lee el archivo .env

# Si modificas estos alcances, asegúrate de borrar el archivo token.json
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

# Define la ruta de la plantilla de correo HTML
TEMPLATE_PATH_PROVEEDOR = os.path.join(os.path.dirname(__file__), 'mails/mail_alta_proveedor.html')
TEMPLATE_PATH_CLIENTE = os.path.join(os.path.dirname(__file__), 'mails/mail_alta_cliente.html')

def get_credentials():
    creds = None

    token_json = env("GOOGLE_TOKEN", default=None)
    #token_json = 'token.json'
    
    # Leer credenciales desde el archivo token.json si existe
    if token_json:
        creds = Credentials.from_authorized_user_file(token_json, SCOPES)
    
    # Si no existen credenciales o son inválidas, intenta refrescarlas
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Usa las variables de entorno para crear las credenciales
            creds = Credentials(
                None,
                refresh_token=env('GOOGLE_OAUTH2_REFRESH_TOKEN'),
                token_uri='https://oauth2.googleapis.com/token',
                client_id=env('GOOGLE_OAUTH2_CLIENT_ID'),
                client_secret=env('GOOGLE_OAUTH2_CLIENT_SECRET')
            )
            creds.refresh(Request())
        # Guardar el nuevo token en token.json
        with open(token_json, 'w') as token:
            token.write(creds.to_json())
    
    return creds

def send_mail_alta_proveedor(proveedor, email):
    try:
        # Obtener las credenciales de Gmail
        creds = get_credentials()
        service = build('gmail', 'v1', credentials=creds)

        # Renderizar la plantilla HTML utilizando el sistema de plantillas de Django
        html_content = render_to_string('mails/mail_alta_proveedor.html', {
            'proveedor': proveedor
        })

        # Crear el mensaje MIME
        message = MIMEMultipart('alternative')
        message['to'] = email
        message['subject'] = f'Solicitud de alta finalizada, {proveedor}!'
        
        # Añadir el contenido HTML
        message_html = MIMEText(html_content, 'html')
        message.attach(message_html)

        # Convertir el mensaje a base64
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        # Enviar el correo utilizando la API de Gmail
        create_message = {'raw': raw_message}
        send_message = service.users().messages().send(userId="me", body=create_message).execute()
        print(f'Mensaje enviado: {send_message["id"]}')
    
    except HttpError as error:
        print(f'Error al enviar email al proveedor: {error}')

def send_mail_alta_cliente(cliente, email):
    try:
        creds = get_credentials()
        service = build('gmail', 'v1', credentials=creds)

        # Renderizar la plantilla utilizando el sistema de plantillas de Django
        html_content = render_to_string('mails/mail_alta_cliente.html', {'cliente': cliente})

        # Crear el mensaje MIME
        message = MIMEMultipart('alternative')
        message['to'] = email
        message['subject'] = f'Solicitud de alta finalizada, {cliente}!'
        message_html = MIMEText(html_content, 'html')
        message.attach(message_html)

        # Convertir el mensaje a base64
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        # Enviar el correo
        create_message = {'raw': raw_message}
        send_message = service.users().messages().send(userId="me", body=create_message).execute()
        print(f'Mensaje enviado: {send_message["id"]}')
    
    except HttpError as error:
        print(f'Error al enviar email al usuario: {error}')

def send_mail_nuevo_pedido(pedido):
    try:
        # Obtener las credenciales para Gmail
        creds = get_credentials()
        service = build('gmail', 'v1', credentials=creds)

        # Renderizar la plantilla utilizando el sistema de plantillas de Django
        html_content = render_to_string('mails/mail_nuevo_pedido.html', {
            'pedido': pedido,
            'items': pedido.items.all(),
            'total': pedido.total(),
        })

        # Crear el mensaje MIME
        message = MIMEMultipart('alternative')
        message['to'] = pedido.cliente.usuario.email
        message['subject'] = f'Pedido recibido! #{pedido.id}'
        message_html = MIMEText(html_content, 'html')
        message.attach(message_html)

        # Convertir el mensaje a base64
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        # Enviar el correo utilizando la API de Gmail
        create_message = {'raw': raw_message}
        send_message = service.users().messages().send(userId="me", body=create_message).execute()
        print(f'Mensaje enviado: {send_message["id"]}')
    
    except HttpError as error:
        print(f'Error al enviar email al usuario: {error}')



def send_mail_pedido_confirmado(pedido):
    try:
        # Obtener las credenciales para Gmail
        creds = get_credentials()
        service = build('gmail', 'v1', credentials=creds)

        # Renderizar la plantilla utilizando el sistema de plantillas de Django
        html_content = render_to_string('mails/mail_pedido_confirmado.html', {
            'pedido': pedido,
            'items': pedido.items.all(),
            'total': pedido.total(),
        })

        # Crear el mensaje MIME
        message = MIMEMultipart('alternative')
        message['to'] = pedido.cliente.usuario.email
        message['subject'] = f'Pedido confirmado! #{pedido.id}'
        message_html = MIMEText(html_content, 'html')
        message.attach(message_html)

        # Convertir el mensaje a base64
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        # Enviar el correo utilizando la API de Gmail
        create_message = {'raw': raw_message}
        send_message = service.users().messages().send(userId="me", body=create_message).execute()
        print(f'Mensaje enviado: {send_message["id"]}')
    
    except HttpError as error:
        print(f'Error al enviar email al usuario: {error}')