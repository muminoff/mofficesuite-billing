#!/usr/bin/env python

# import smtplib

# sender = "billing@mofficesoft.com"
# receivers = ["linuxmaster@hanbiro.com"]

# message = "Test"

# try:
#     server = smtplib.SMTP('hanbiro.net', 25)
#     # smtpObj.login("billing", "qlffld!!")
#     server.set_debuglevel(2)
#     server.ehlo()
#     server.starttls()
#     server.sendmail(sender, receivers, message)
#     print "Sent mail"
# except smtplib.SMTPException as e:
#     print "Unable to send mail", e


import smtplib
 
to = 'sardor@hanbiro.com'
mail_user = 'billing@mofficesoft.com'
mail_pwd = ''
smtpserver = smtplib.SMTP("hanbiro.net",25)
smtpserver.ehlo()
smtpserver.starttls()
smtpserver.ehlo
smtpserver.login(mail_user, mail_pwd)
header = 'To:' + to + '\n' + 'From: ' + mail_user + '\n' + 'Subject:testing \n'
print header
msg = header + '\n this is test msg from billing \n\n'
smtpserver.sendmail(mail_user, to, msg)
print 'done!'
smtpserver.close()
