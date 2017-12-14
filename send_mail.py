# Author Muhammad Faheem Khan
# Date: 12/12/2017
# File name: test_mail.py
# Description: This program opens todays task list file created before this file is called and emails the data

# modules
import smtplib
from email.mime.text import MIMEText
import os
import datetime

# this function puts the message together
def msg(fname):
    # generating html template
    pre_msg = "<table ><tr><th>Date</th><thstyle='background: #dadee5;'>Time</th><th>Activity</th></tr>"
    message = "\n"
    with open(fname, "r") as f: # opening todays file
        content = sorted(f.readlines())
        for i in content:
            i = i.replace("/", " ") # [[],[],[]]
            message += "<tr><td>" + i[:10] + "</td>"
            message += "<td style='background: #dadee5;'>" + i[11:15] + "</td>"
            message += "<td>" + i[16:] + "</td></tr>"
        message += "</table>"
        message += "<h3>This email is sent using python3</h3>"
        message = pre_msg + message
        # print(message)
        return message

# this function sends the email
def send_mail(email, fname):
    title = 'Your Tasks for Today'
    msg_content = msg(fname) # calling the msg() to get the html template
    message = MIMEText(msg_content, 'html')

    message['From'] = '<Sender Email>'
    message['To'] = email
    message['Cc'] = '<Sender/Reciver Email>'
    message['Subject'] = 'Your Tasks for Today'

    msg_full = message.as_string()

    server = smtplib.SMTP('smtp.gmail.com:587') # SMTP server settings
    server.starttls() # asking the google server for permission to connect
    server.login('Sender email', 'Password') # login credentials
    server.sendmail('Sender email', 'Reciver email', msg_full) # sending email
    server.quit() # disconneting from the user
