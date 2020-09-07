import smtpd
import smtplib
from email.message import EmailMessage

import os
import decouple

def send_mail(text_message):
    email_address = 'myothiha.kyaw@mm-digital-solutions.com'
    email_pass = 'blackeye.mmr3345'
    
    contacts = ['mthk97.mc@gmail.com','thethlaing@mm-digital-solutions.com']
    msg = EmailMessage()
    msg['Subject'] = 'Crawler Error Message'
    msg['From'] = email_address
    msg['To'] = ','.join(contacts)
    msg.set_content(text_message)

    with smtplib.SMTP_SSL('smtp.gmail.com',465) as smt:
        smt.login(email_address,email_pass)
        smt.send_message(msg)