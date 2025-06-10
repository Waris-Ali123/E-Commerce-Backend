import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def sending_email_with_token(sender,password,receiver,reset_token,receiver_name):

    subject_line = "Password Reset Token for E-commerce login"
    
    body = f"""
Dear {receiver_name},

Thank you for visiting our site.

Here is your password reset token:

    {reset_token}

⚠️ Please note: This token is valid for **5 minutes** only. After that, it will expire for your security.

If you did not request this, please ignore this message.

Warm regards,  
Support Team
"""

    msg  = MIMEMultipart()

    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject_line

    msg.attach(MIMEText(body,"plain"))


    try:
        with smtplib.SMTP("smtp.gmail.com",587) as my_server:
            my_server.starttls()
            my_server.login(sender,password)
            my_server.sendmail(sender,receiver,msg.as_string())
            print("email sent successfully")

    except Exception as e:
        print("Error in sending mail : ",e)
        raise
