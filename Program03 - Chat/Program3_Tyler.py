from ftplib import FTP

# FTP server details
IP = "138.47.99.64"
PORT = 21
USER = "anonymous"
PASSWORD = ""
METHOD = "7" 			# change to either 10 or 7 to do 10-bit or 7-bit conversion
FOLDER = "/"
USE_PASSIVE = True		# set to False if the connection times out

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

# Converts the file permission (first 10 char) into 10-bit or 7-bit binary
def binaryConversion(file, bitSize):
	binaryStr = ""

	# Conditional; checks "bitSize" to see what to convert file "file" into
	# Converts file "file" to 10-bit binary
	if bitSize == "10":
		for char in range(0, 10):	# Looks at the first 10 chars
			if file[char] == "-":	# if it sees a "-"
				binaryStr += "0"	# append a string binary 0 to string "binaryStr"
			else:					# if it doesn't see a "-"
				binaryStr += "1"	# append a string binary 1 to string "binaryStr"

	# Converts file "file" to 7-bit binary
	elif bitSize == "7":
		if file[0:3] == "---":			# Checks if the first 3 chars is "---"
			for char in range (3, 10):	# if it does, look at the next 7 chars after
				if file[char] == "-":	# if it sees a "-"
					binaryStr += "0"	# append a string binary 0 to string "binaryStr"
				else:					# if it doesn't see a "-"
					binaryStr += "1"	# append a string binary 1 to string "binaryStr"
	
	# Throws an error if "bitSize" is not "10" or "7"
	else:
		print(f"ERROR: {bitSize} is not a valid bit size")
		quit()
	return binaryStr

# Converts binary to ASCII
def asciiConversion(binaryStr):
	def recursive(binaryStr):
		nonlocal asciiText

		# Will ValueError because cannot convert empty string into a int
		try:
			charBit = int(binaryStr[0:7], 2)	# Gets the first 7 chars and converts into a int with base 2
			asciiText += chr(charBit)			# Converts that into ascii and append it to asciiText
			reducedbinaryStr = binaryStr[7:]	# Removes the first 7 chars of string "binaryStr"
			recursive(reducedbinaryStr)			# Recursion
		except ValueError:
			pass

	asciiText = ""
	recursive(binaryStr) # Start recursion process
	return asciiText

binaryStr = ""

for f in files:
	binaryStr += binaryConversion(f, METHOD)

asciiText = asciiConversion(binaryStr)
print(asciiText)
