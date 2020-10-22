import smtpd
import smtplib
from email.message import EmailMessage

import os
import decouple

def send_mail(text_message):
    email_address = 'th.ucsy@gmail.com'
    email_pass = 'tnkutpvjiyxrbgqo'
    
    contacts = ['thethlaing@mm-digital-solutions.com']
    msg = EmailMessage()
    msg['Subject'] = 'Carsnet Crawler had an issue and suddently stoppped!'
    msg['From'] = email_address
    msg['To'] = ','.join(contacts)
    msg.set_content(text_message)

    with smtplib.SMTP_SSL('smtp.gmail.com',465) as smt:
        smt.login(email_address,email_pass)
        smt.send_message(msg)