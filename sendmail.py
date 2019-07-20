import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
mail_content = '''Good morning,Concierge Team
This is automatic Snow Report Create by IQ.
If you recive this one can you reply back plz.
It is a simple snow report i will try to improve it.

Thank You
Nuttapong Chaiyawong(IQ) :)
'''
#The mail addresses and password
sender_address = '....@gmail.com' #gmail
sender_pass = '.....' #password_gmail
receiver_address = '....' #destination
#Setup the MIME
message = MIMEMultipart()
message['From'] = sender_address
message['To'] = receiver_address
message['Subject'] = 'Today Snow Report by _NTPQ'
#The subject line
#The body and the attachments for the mail
message.attach(MIMEText(mail_content, 'plain'))
attach_file_name = 'form_letter.pdf'
attach_file = open(attach_file_name, 'rb') # Open the file as binary mode
payload = MIMEBase('application', 'octate-stream')
payload.set_payload((attach_file).read())
encoders.encode_base64(payload) #encode the attachment
#add payload header with filename
payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
message.attach(payload)
#Create SMTP session for sending the mail
session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
session.starttls() #enable security
session.login(sender_address, sender_pass) #login with mail_id and password
text = message.as_string()
session.sendmail(sender_address, receiver_address, text)
session.quit()
print('Mail Sent')