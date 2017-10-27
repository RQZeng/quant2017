#!/usr/bin/env python  
# -*- coding: UTF-8 -*-  
   
from email.mime.multipart import MIMEMultipart  
from email.mime.base import MIMEBase  
from email.mime.text import MIMEText  
   
# python 2.3.*: email.Utils email.Encoders  
from email.utils import COMMASPACE,formatdate  
from email import encoders  
from email.header import Header
   
import os  
   
#server['name'], server['user'], server['passwd']  
def send_mail(server, fro, to, subject, text, files=[]):   
	assert type(server) == dict   
	assert type(to) == list   
	assert type(files) == list

	msg = MIMEMultipart()
	msg['From'] = Header(fro,'utf-8')
	msg['Subject'] = Header(subject,'utf-8')
	msg['To'] = COMMASPACE.join(to)
	msg['Date'] = formatdate(localtime=True)
	msg.attach(MIMEText(text,'plain','utf-8'))
	
	for file in files:
		part = MIMEBase('application', 'octet-stream') #'octet-stream': binary data
		part.set_payload(open(file, 'rb'.read()))
		encoders.encode_base64(part)
		part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
		msg.attach(part)
		
	import smtplib
	smtp = smtplib.SMTP()
	smtp.connect(server['name'],25)
	smtp.login(server['user'], server['passwd'])
	smtp.sendmail(fro, to, msg.as_string())
	smtp.close()  


# SERVER['name'] = 'smtp.126.com'
# SERVER['user'] = 'wusion@126.com'
# SERVER['passwd'] = '$Wusion09rq10.'
SERVER={
	'name':'smtp.126.com',
	'user':'wusion@126.com',
	'passwd':'$Wusion09rq10.'
}
fro='wusion@126.com'
to=['wusion@126.com','330393974@qq.com']
subject='这是标题吗'
text='test test 这是内容啊'

#send_mail(SERVER,fro,to,subject,text)

def SendMail(msub,mtext):
	send_mail(SERVER,fro,to,msub,mtext)
