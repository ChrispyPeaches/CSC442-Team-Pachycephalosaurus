# use Python 3
import socket
from sys import stdout
from time import time

# enables debugging output
DEBUG = True

# set the server's IP address and port
ip = "138.47.99.64"
port = 31337


# create the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the server
s.connect((ip, port))

times = []
# receive data until EOF
data = s.recv(4096).decode()
t0 = time()
data = s.recv(4096).decode()
t1 = time()
# calculate the time delta (and output if debugging)
delta = round(t1 - t0, 3)
#times.append(delta)


while (data.rstrip("\n") != "EOF"):
	# output the data
	stdout.write(data)
	stdout.flush()
	# start the "timer", get more data, and end the "timer"
	t0 = time()
	data = s.recv(4096).decode()
	t1 = time()
	# calculate the time delta (and output if debugging)
	delta = round(t1 - t0, 3)
	times.append(delta)

	if (DEBUG):
		stdout.write(" {}\n".format(delta))
		stdout.flush()

print("times[0] = " + str(times[0]))
# Match the first time delay with either .1 or .05
if times[0] > .075 and times[0] < .150:
	time1 = 0.05
else:
	time1 = 0.1
print("time1 = " + str(time1)
)

binary = []
# Use the first time to determine which time represents which bit throughout delta
for i in range(len(times)):
	# Checks if time[i] is in the range of time1
	if (time1 < times[i]+0.024) and (time1 > times[i]-0.024):
		binary.append('0')
	else:
		binary.append('1')

print(binary)

# convert binary list to characters
for i in range(0,len(binary),8):
	# split list into bytes
	byte = binary[i:i+8]
	character = chr(int(''.join(byte),2))
	
	print(character)
	
# close the connection to the server
s.close()

#'1', '1', '1', '0', '0', '0', '1', '1', '0', '0', '0', '0', '0', '1', '1', '1', '0', '0', '0', '1', '0', '1', '1', '1', '0', '0', '0', '1', '0', '1', '1', '1', '0', 