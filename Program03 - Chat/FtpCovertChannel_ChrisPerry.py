from ftplib import FTP

# FTP server details
IP = "138.47.136.89"
PORT = 21
USER = "ianmalcolm"
PASSWORD = "jurassicpark"
FOLDER = "/files/10"
USE_PASSIVE = True # set to False if the connection times out
METHOD = 10
files = []

# connect and login to the FTP server
with FTP() as ftp:
	ftp.connect(IP, PORT)
	ftp.login(USER, PASSWORD)
	ftp.set_pasv(USE_PASSIVE)

	# navigate to the specified directory and list files
	ftp.cwd(FOLDER)
	ftp.dir(files.append)

	# exit the FTP server
	ftp.quit()

# display the folder contents
def decryptPerms(files, METHOD):
	message_bin = ""
	METHOD = 7
	for f in files:
		# Isolate permissions string
		filePerms = str(f.split(" ")[0])
		# If using 7-bit MODE, filter out permissions with first 3 bits unset
		if filePerms[0:3] != "---":
			METHOD = 7
		# If using 7-bit method, use only the rightmost 7 bits
		filePerms = filePerms if METHOD == 10 else filePerms[3:]

		# Convert permissions to binary representations
		filePerms_bin = ""
		for ch in filePerms:
			filePerms_bin += '1' if ch != '-' else '0'

		message_bin += filePerms_bin

# Convert the message from binary to ascii representation
def printMessage(message_bin):
	message = ""
	for i in range(0, len(message_bin), 7):
		message += chr(int(f'0b{message_bin[i:i+7]}', 2))
	print(message)

message_bin_7 = decryptPerms(files, 7)
message_bin_10 = decryptPerms(files, 10)
printMessage(message_bin_7)
printMessage(message_bin_10)
