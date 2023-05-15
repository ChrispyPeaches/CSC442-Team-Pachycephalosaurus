
from ftplib import FTP

# if method is true, 7 bit decoding is active / if flase, 10 bit is active
METHOD = False

# FTP server details
#IP = "localhost"
IP = "138.47.99.64"
PORT = 21
USER = "anonymous"
PASSWORD = ""
FOLDER = "/10"
USE_PASSIVE = True # set to False if the connection times out

# connect and login to the FTP server
ftp = FTP()
ftp.connect(IP, PORT)
ftp.login(USER, PASSWORD)
ftp.set_pasv(USE_PASSIVE)

# navigate to the specified directory and list files
ftp.cwd(FOLDER)
files = []
ftp.dir(files.append)

# exit the FTP server
ftp.quit()

bin = []

for f in files:
	for c in f[0:10]:
		
		if c=="-":
			bin.append("0")
		elif c=="r" or c=="w" or c=="x":
			bin.append("1")
		else:
			if METHOD==True:
				bin.append("0")
			else:
				bin.append("1")



# At this point, bin is the list of all bits coresponding to the file permissions
if METHOD==True:
	
	step = 10
	for i in range(0, len(bin), step):

		
		if  bin[i:i+3] == ['0','0','0']:
			L = bin[i+3:i+step]
			character = chr(int("".join(L),2))

			print(character)

else:
	step = 7
	for i in range(0, len(bin), step):
		L = bin[i:i+step]
		
		character = chr(int("".join(L),2))

		print(character)
			
	
	


	

	



