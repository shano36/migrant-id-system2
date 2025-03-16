from django.core.mail import send_mail
from django.conf import settings
from twilio.rest import Client

def send_status_email(application):
    subject = f"Application Status Update - {application.name}"
    message = f"""
    Dear {application.name},

    Your application status has been updated to: {application.status}.
    
    If you have any questions, please contact support.

    Thank you!
    """
    recipient = application.email

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient])


def send_status_sms(application):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    message_body = f"Hello {application.name}, your application status is now: {application.status}."

    client.messages.create(
        body=message_body,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=application.phone
    )
