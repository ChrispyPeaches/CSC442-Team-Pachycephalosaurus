import socket
from sys import stdout
from time import time

DEBUG = False
THRESH = 0.075 # threshold value for timing (less than THRESH means 0)

ip = '138.47.99.64' # server's IP and port
port = 31337

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create socket
s.connect((ip, port)) # connect to server

deltas = []
# receive data until EOF
data = s.recv(4096).decode()
while( data.rstrip("\n") != "EOF" ):
    stdout.write(data) # output data
    stdout.flush()
    
    t0 = time() # start time
    data = s.recv(4096).decode() # receive data
    delta = round(time() - t0, 3) # time delta of the received data
    deltas.append(delta) # append to delta list
    if(DEBUG): # output time deltas
        stdout.write(" {}\n".format(delta))
        stdout.flush()    

s.close() # disconnect from the server after receiving "EOF"

covertBin = ""
for bit in deltas: # build binary string from stored time deltas
    if( bit <= THRESH ): # compare to threshold time
        covertBin += '0' # less than THRESH means 0
    else:
        covertBin += '1'

output = ""
if(len(covertBin)%7 == 0): # detect whether it's 7 or 8-bit ASCII
    byteSize = 7
else:
    byteSize = 8 # default of 8-bit
for i in range(int(len(covertBin)/byteSize)): # convert from binary to ASCII
    output += chr(int(covertBin[ (i*byteSize):((i+1)*byteSize) ], 2))
    
if(DEBUG): # provide binary and original output
    stdout.write("Binary:\n" + covertBin + "\n") # stdout might be "more correct" than print?
    stdout.write("Raw output:\n" + output + "\n")

if( output.find("EOF") != -1 ): # if EOF is found
    stdout.write( output[:output.find("EOF")] + "\n") # output everything before the EOF
else:
    stdout.write("Error finding EOF in output:\n" + output + "\n") # or do the raw output
