
from ftplib import FTP

# FTP server details
IP = "localhost"
PORT = 21
USER = "anonymous"
PASSWORD = ""
FOLDER = "/"
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

# display the folder contents
for f in files:
	print(f)
