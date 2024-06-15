from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL

from src.config import settings


def send_email(
    mail_server: SMTP_SSL,
    recipients: list[str],
    subject: str,
    text: str,
):
    if not recipients:
        return
    message = MIMEMultipart()
    message["From"] = settings.mail_server.login
    message["To"] = ", ".join(recipients)
    message["Subject"] = subject
    text = MIMEText(_text=text)
    message.attach(payload=text)
    full_message = message.as_string()
    mail_server.sendmail(
        from_addr=message["From"],
        to_addrs=recipients,
        msg=full_message,
    )


def get_mail_server() -> SMTP_SSL:
    mail_server = SMTP_SSL(
        host=settings.mail_server.host,
        port=settings.mail_server.port,
    )
    mail_server.login(
        user=settings.mail_server.login,
        password=settings.mail_server.password,
    )
    return mail_server


def mail_server_quit(mail_server: SMTP_SSL):
    mail_server.quit()
