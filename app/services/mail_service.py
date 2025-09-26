from flask_mail import Message
from flask import current_app

def send_email(to, subject, template):
    if current_app.config.get('TESTING'):
        return

    mail = current_app.extensions.get('mail')
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)