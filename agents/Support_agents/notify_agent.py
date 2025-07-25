'''Purpose: sending notification via email/whatsapp when a ticket is created or action is taken and in need of attention.'''
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class send_mail:
    def send_email_via_sendgrid(from_email,to_emails,subject,text_content):
        message = Mail(
            from_email=from_email,
            to_emails=to_emails,
            subject=subject,
            html_content = f"<strong>{text_content}<>/strong")
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            return True
        except Exception as e:
            # print(e.message)
            return False

