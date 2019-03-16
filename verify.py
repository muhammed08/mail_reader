import re
import smtplib
import dns.resolver
def verify_mail(addressToVerify):
	# Address used for SMTP MAIL FROM command  
	fromAddress = 'muhammedameen08@gmail.com'

	# Simple Regex for syntax checking
	regex = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$'


	

	# Syntax check
	match = re.match(regex, addressToVerify)
	if match == None:
		print('Bad Syntax')
		print(addressToVerify)
		raise ValueError('Bad Syntax')

	# Get domain for DNS lookup
	splitAddress = addressToVerify.split('@')
	domain = str(splitAddress[1])
	print('Domain:', domain)

	# MX record lookup
	records = dns.resolver.query(domain, 'MX')
	mxRecord = records[0].exchange
	mxRecord = str(mxRecord)


# SMTP lib setup (use debug level for full output)
	server = smtplib.SMTP()
	server.set_debuglevel(0)

	# SMTP Conversation
	server.connect(mxRecord)
	server.helo(server.local_hostname) ### server.local_hostname(Get local server hostname)
	server.mail(fromAddress)
	try:
		code, message = server.rcpt(str(addressToVerify))
		if code == 250:
			return True
		else:
			return False
	except:
		return True
	server.quit()

	#print(code)
	#print(message)

	# Assume SMTP response 250 is success
	