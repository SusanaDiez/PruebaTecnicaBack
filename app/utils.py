import requests
from twilio.rest import Client
from app.config import settings
import logging

logger = logging.getLogger(__name__)

def enviar_email(destinatario: str, asunto: str, mensaje: str):
    try:
        response = requests.post(
            f"https://api.mailgun.net/v3/{settings.MAILGUN_DOMAIN}/messages",
            auth=("api", settings.MAILGUN_API_KEY),
            data={"from": settings.MAILGUN_FROM_EMAIL,
                  "to": [destinatario],
                  "subject": asunto,
                  "text": mensaje})
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Error al enviar el correo: {e}")
        raise RuntimeError("Error al enviar el correo electrónico") from e

def enviar_sms(destinatario: str, mensaje: str):
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=mensaje,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=destinatario
        )
    except Exception as e:
        logger.error(f"Error al enviar el SMS: {e}")
        raise RuntimeError("Error al enviar el SMS") from e
