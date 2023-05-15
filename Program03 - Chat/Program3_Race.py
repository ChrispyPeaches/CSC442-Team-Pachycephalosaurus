from ftplib import FTP

# FTP server details
IP = "138.47.99.64"
PORT = 21
USER = "anonymous"
PASSWORD = ""
FOLDER = "/10" # "/7" or "/10" for 7/10-bit method
USE_PASSIVE = True # set to False if the connection times out
METHOD = "10-bit" # use either "7-bit" or "10-bit"

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
### Code above this line taken from Moodle (except 'METHOD' line)

# process the file permission information
binOut = ""
for line in files: 
    byte = ""
    if( (METHOD == "7-bit") and (line[0:3] == '---')):      
        byte = line[3:10] # ignore first three 'bits' of permissions
    elif(METHOD == "10-bit"):
        byte = line[:10] # take all ten 'bits'
    
    # convert to binary
    binByte = ""
    for i in range(len(byte)): 
        if(byte[i] == '-'):
            binByte += '0' # '-' means zero
        else:
            binByte += '1' # anything else is one
    binOut += binByte

# get ASCII from binary
output = ""
for i in range(int(len(binOut)/7)):
    output += chr(int(binOut[ (i*7):((i+1)*7) ], 2))
    
print(output)
