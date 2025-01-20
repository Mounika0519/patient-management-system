import smtplib
from smtplib import SMTP 
from email.message import EmailMessage

def sendemail(to,subject,body):
    server=smtplib.SMTP_SSL('smtp.gmail.com',465)
    server.login('karnemounika05@gmail.com','ndgf ukcm pksc ztvq')
    msg=EmailMessage()
    msg['From']='karnemounika05@gmail.com'
    msg['Subject']=subject
    msg['To']=to
    msg.set_content(body)
    server.send_message(msg)
    server.quit()