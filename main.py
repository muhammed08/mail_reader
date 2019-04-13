import getmail
import pyttsx3    #to speak
import os		
from pathlib import Path
import playsound 	#play music
import speech_recognition as sr
import verify
import email
import imaplib
import html2text
r=sr.Recognizer()

def getmessagelist(mailid,password,flag):   #flag=0 for unseen messages and 1 for seen messages
	server=imaplib.IMAP4_SSL('imap.gmail.com')
	HOST = 'imap.gmail.com'
	USERNAME = mailid
	PASSWORD = password
	server.login(USERNAME, PASSWORD)
	server.select("inbox", readonly=True)
	if(flag==0):
		(result,messages) = server.uid('search','UNSEEN')
	else
		(result,messages) = server.uid('search','SEEN')
	message_list=messages[0].split()
	return message_list

def readdetailsmail(email_message):
	

def play_audio(filename):
	playsound.playsound(filename, True)

def saysomething(textval):
	engine = pyttsx3.init()
	engine.say(textval)
	engine.setProperty('rate',100)
	engine.setProperty('volume', 0.9)
	engine.runAndWait()

def initSpeech():
	check=True
	while(check):
		play_audio("start.mp3")
		with sr.Microphone() as source:
			print("say something")
			audio=r.listen(source)
		play_audio("end.mp3")
		try:
			command=r.recognize_google(audio)
			check=False
		except:
			saysomething("Sorry..., could't catch that")
	print("You said "+command)
	return command



def create_basefile():
	file=open("init.txt","w")
	file.write("program used already")
	file.close()

def changemail():
	emailid=getEmail()
	password=getPassword()
	file=open("log.txt","w")
	file.write(emailid+"\n")
	file.write(password)
	file.close()

def getEmail():
	check=True;
	while(check):
		saysomething("Please tell me your email id")
		emailid=initSpeech()
		saysomething("your email id is  :"+emailid)
		saysomething("Do you want to change that ?")
		decision=initSpeech()
		if(decision!="yes" or decision !="s" ):
			check=False

	return emailid;
def encrypt(eid,password):
	passw=password
	for i in range(0,len(password)):
		passw[i]=password[i]-eid[i]
	return password

def decrypt(eid,password):
	passw=password
	for i in range(0,len(password)):
		passw[i]=password[i]-eid[i]
	return password
def getPassword():
	check=True;
	while(check):
		saysomething("Please tell me your password")
		password=initSpeech()
		saysomething("your password is  :"+password)
		saysomething("Do you want to change that ?")
		decision=initSpeech()
		if(decision!="yes" or decision !="s" ):
			check=False

	return password;

r=sr.Recognizer()



def checkmail(mailid,password):
	message_list=getmessagelist(mailid,password,0)
	saysomething("You have "+str(len(message_list))+"  new emails")
	saysomething("D you want me to read new emails   ?")
	command=initSpeech()
	if "yes" in command:
		check=True
		saysomething("reading the latest new mail")
	else:
		check=False
	i=-1;
	while(check):
		new_mail=message_list[i]
		result2,email_data=server.uid('fetch',new_mail,'(RFC822)')
		raw_email=email_data[0][1].decode("utf-8")
		email_message=email.message_from_string(raw_email)
		saysomething("The date of mail is " + str(email_message['Date']))
		saysomething("the message is from "+email_message['From'])
		saysomething(" And The subject of mail is "+email_message['Subject'])
		saysomething("Do you want to read contents of mail?")
		command=initSpeech()
		if "yes" in command or "yup" in command :
			try:
				email_cont=html2text.html2text(email_message.get_payload())
				for chara in "!@#$%^&*_-":
					email_cont=email_cont.replace(chara," ")
				saysomething(email_cont)
			except:
				for part in email_message.walk():
					if(part.get_content_type() == 'text/plain'):
						email_cont=part.get_payload()
						for chara in "!@#$%^&*_-":
							email_cont=email_cont.replace(chara," ")
						saysomething(email_cont)
				
		i=i-1
		if(i*-1 > len(message_list)):
			saysomething("Thats all for today")
			check=False
		else:
			saysomething("Do you want me to read the next mail?")
			command=initSpeech()
			if "yes" in command or "yeah" in command:
				check=True
			else:
				check=False
    

def sendmail(mailid,password):
	import smtplib
	conn=smtplib.SMTP('smtp.gmail.com',587)
	conn.ehlo()
	conn.starttls()
	conn.login(mailid,password)
	saysomething("Please tell the senders valid email address  :")
	sendadd=initSpeech()
	sendadd.replace(" ","")
	addrcheck=verify.verify_mail(sendadd)
	print(sendadd)
	if(addrcheck):
		print("valid mail");
	else:
		print("invalid mail")
		exit()
	saysomething("Tell me Subject of mail  :")
	sub=initSpeech()
	saysomething("tell me the contents of the mail")
	content=initSpeech()
	conn.sendmail(mailid,sendadd,'Subject:'+sub+'\n\n'+content)
	conn.quit()
	try:
		saysomething("mail has been send")
	except smtplib.SMTPRecipientsRefused:
		saysomething("Senders email id is not valid")


def searchmail(mailid,password):
	message_list=getmessagelist(mailid,password,0)  #get unread message list
	len1=min(len(message_list),50)
	message_list=message_list[len(message_list)-len1:]
	message_list1=getmessagelist(mailid,password,1)    #get read message list
	len2=min(len(message_list1),50)
	message_list=message_list[len(message_list1)-len2:]
	message_list=message_list+message_list1
	#saysomething("You have "+str(len(message_list))+"  new mails")
	#saysomething("The latest one is ")
	saysomething("Tell me the what to search for. The keywords available are  :")
	saysomething("Date : for searching a mail at that date, To: The to address, Keyword: for searching that particular word in any of recent mails ")
	saysomething("From : for mails from that from address")
	search_command=initSpeech()
	"""if "date" in search_command:
		saysomething("Please tell the date to search for  :")"""
	if "to" in search_command:
		saysomething("Please tell the to address")
	elif "from" in search_command:
		saysomething("Please tell the from address")
	else:
		saysomething("Pleasetell me the keyword to search for  :")
	keyword_search=initSpeech()
	"""if "date" in search_command:
		keyword_search=convert_date(keyword_search)"""

	i=-1;
	check=True
	while(check):
		print("checking "+ str(-1*i) +" message")
		seen=False
		new_mail=message_list[i]
		result2,email_data=server.uid('fetch',new_mail,'(RFC822)')
		raw_email=email_data[0][1].decode("utf-8")
		email_message=email.message_from_string(raw_email)

		########################   date cheking            ###########################

		#need some standerd

		"""if "date" in search_command and email_message['Date']==keyword_search:
			saysomething("One mail found with said match")
			saysomething("The details of the mail is   :")
			saysomething("the message is from "+email_message['From'])
			saysomething(" And The subject of mail is "+email_message['Subject'])
			saysomething("Do you want to read contents of mail?")
			command=initSpeech()
			if "yes" in command or "yup" in command :
				try:
					email_cont=html2text.html2text(email_message.get_payload())
					for chara in "!/+=#$%^&*_-":
						email_cont=email_cont.replace(chara," ")
					saysomething(email_cont)
				except:
					for part in email_message.walk():
						if(part.get_content_type() == 'text/plain'):
							email_cont=part.get_payload()
							for chara in "!/+=#$%^&*_-":
								email_cont=email_cont.replace(chara," ")
							saysomething(email_cont)"""
		if "from" in search_command and email_message['From']==keyword_search:
			seen=True
			saysomething("One mail found with said match")
			saysomething("The details of the mail is   :")
			saysomething("the message date is "+email_message['Date'])
			saysomething(" And The subject of mail is "+email_message['Subject'])
			saysomething("Do you want to read contents of mail?")
			command=initSpeech()
			if "yes" in command or "yup" in command :
				try:
					email_cont=html2text.html2text(email_message.get_payload())
					for chara in "!/+=#$%^&*_-":
						email_cont=email_cont.replace(chara," ")
					saysomething(email_cont)
				except:
					for part in email_message.walk():
						if(part.get_content_type() == 'text/plain'):
							email_cont=part.get_payload()
							for chara in "!/+=#$%^&*_-":
								email_cont=email_cont.replace(chara," ")
							saysomething(email_cont)
		
		if "to" in search_command and email_message['To']==keyword_search:
			seen=True
			saysomething("One mail found with said match")
			saysomething("The details of the mail is   :")
			saysomething("the date of message is "+email_message['Date'])
			saysomething(" And The subject of mail is "+email_message['Subject'])
			saysomething("Do you want to read contents of mail?")
			command=initSpeech()
			if "yes" in command or "yup" in command :
				try:
					email_cont=html2text.html2text(email_message.get_payload())
					for chara in "!/+=#$%^&*_-":
						email_cont=email_cont.replace(chara," ")
					saysomething(email_cont)
				except:
					for part in email_message.walk():
						if(part.get_content_type() == 'text/plain'):
							email_cont=part.get_payload()
							for chara in "!@#$%^&*_-":
								email_cont=email_cont.replace(chara," ")
							saysomething(email_cont)
		if "keyword" in search_command:
			
			try:
				email_cont=html2text.html2text(email_message.get_payload())
				for chara in "!/+=#$%^&*_-":
					email_cont=email_cont.replace(chara," ")
				print("Searching for mail from  :"+email_message['From'])
				if keyword_search in email_cont:
					seen=True
					saysomething("One mail found with said match")
					saysomething("The details of the mail is   :")
					saysomething("the message is from "+email_message['From'])
					saysomething("the message is to "+email_message['To'])
					saysomething("the date of message is "+email_message['Date'])
					saysomething(" And The subject of mail is "+email_message['Subject'])
					saysomething("Do you want to read contents of mail?")
					command=initSpeech()
					if "yes" in command or "yup" in command :
						try:
							email_cont=html2text.html2text(email_message.get_payload())
							for chara in "!/+=#$%^&*_-":
								email_cont=email_cont.replace(chara," ")
								saysomething(email_cont)
						except:
							for part in email_message.walk():
								if(part.get_content_type() == 'text/plain'):
									email_cont=part.get_payload()
									for chara in "!/+=#$%^&*_-":
										email_cont=email_cont.replace(chara," ")
									saysomething(email_cont)

			except:
				for part in email_message.walk():
					if(part.get_content_type() == 'text/plain'):
						email_cont=part.get_payload()
						for chara in "!/+=#$%^&*_-":
							email_cont=email_cont.replace(chara," ")
							if keyword_search in email_cont:
								seen=True
								saysomething("One mail found with said match")
								saysomething("The details of the mail is   :")
								saysomething("the message is from "+email_message['From'])
								saysomething(" And The subject of mail is "+email_message['Subject'])
								saysomething("Do you want to read contents of mail?")
								command=initSpeech()
								if "yes" in command or "yup" in command :
									try:
										email_cont=html2text.html2text(email_message.get_payload())
										for chara in "!/+=#$%^&*_-":
											email_cont=email_cont.replace(chara," ")
										saysomething(email_cont)
									except:
										for part in email_message.walk():
											if(part.get_content_type() == 'text/plain'):
												email_cont=part.get_payload()
												for chara in "!/+=#$%^&*_-":
													email_cont=email_cont.replace(chara," ")
												saysomething(email_cont)

		if(seen):
			saysomething("Do you want to continue searching  :")
			command=initSpeech()
			if "yes" in command:
				check=True
			else:
				check=False
		i=i-1
		if(i*-1 > len(message_list)):
			saysomething("Cannot Find any match")
			check=False





# Check if program is used before
path=os.getcwd()
file_path=path+"\\record.txt"
log_path=path+"\\log.txt"
log_file=Path(log_path)
my_file = Path(file_path)
while(my_file.is_file()==False or log_file.is_file()==False):
	Start.create_basefile()
	emailid=getEmail()
	password=getPassword()
	file=open("log.txt","w")
	file.write(emailid+"\n")
	file.write(password)
	file.close()
check=True
while(check):
	file=open("log.txt","r")
	mailid=file.readline()
	password=file.readline()
	#password=decrypt(mailid,password)
	print(mailid)
	print(password)
	saysomething("Signing in as :"+mailid)
	saysomething("Do you want to sign in with a different account ?")
	command=initSpeech()
	if(command=="yes"):
		changemail()
		file=open("log.txt","r")
		mailid=file.readline()
		password=file.readline()
		saysomething("Signing in as :"+mailid)
	else:
		check=False
#saysomething("checking for new mails.....")
checkmail(mailid,password)
#print(mailid)
#print(password)
check=True;
while(check):
	saysomething("What would you like me to do")
	command=initSpeech()
	if "change" in command:
		changemail();
		continue
	if "send" in command or "sent" in command:
		sendmail(mailid,password)
		continue
	if "search" in command:
		#searchmail(mailid,password)
		continue
	if "refresh" in command or "reload" in command or "check" in command:
		checkmail(mailid,password)







