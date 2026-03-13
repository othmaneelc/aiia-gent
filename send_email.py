import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_gmail(sender_email, app_password, recipient_email, subject, body, html=False):
    if html:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = recipient_email
        # Attach plain text fallback + HTML
        plain = MIMEText("Open in an HTML-compatible email client to view this brief.", "plain", "utf-8")
        rich = MIMEText(body, "html", "utf-8")
        msg.attach(plain)
        msg.attach(rich)
    else:
        msg = MIMEText(body, "plain", "utf-8")
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = recipient_email

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, [recipient_email], msg.as_string())
