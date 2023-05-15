from socket import *
import sys
from sys import stdout
from time import time
from pythonping import ping

ip = "10.4.4.100"
port = 12345
SUSPECTED_DELAY = 0.04
DEBUG = False
LATENCY_ISSUES = False # If set to true, must run with sudo


# Summary: Function to translate binary to ASCII
# Params:
    # covert_bin: binary string to be translated
    # bitsToConvert: number of bits for each character (assumed 7 or 8bit)
# Returns: ASCII string
# Remarks:
    # Translates until "EOF" or "eof" is reached and then 
    # remove that part of the string.
def binaryDecoder(covert_bin, bitsToConvert):
    message = ""
    for i in range(0, len(covert_bin), bitsToConvert):
        message += chr(int(f'0b{covert_bin[i:i+bitsToConvert]}', 2))
        if (message.endswith("EOF") or message.endswith("eof")):
            message = message.replace("EOF", "")
            message = message.replace("eof", "")
            break
        
    return message

# Setup server connection
socket = socket(AF_INET, SOCK_STREAM)
socket.connect((ip, port))

# Decode message and collect covert binary message
covert_binary_msg = ""
data = socket.recv(4096).decode()
while(data.rstrip("\n") != "EOF"):
    # Cleanup stdout
    stdout.write(data)
    stdout.flush()
    # Decode char & get time delta
    t_init = time()
    data = socket.recv(4096).decode()
    t_final = time()

    # If latency is an issue, ping the server and subtract the ping time
    if (LATENCY_ISSUES):
        ping_time = ping(ip, 1, verbose=False).rtt_avg_ms * 10**(-3)
    delta = round(t_final-t_init, 3)
    if (LATENCY_ISSUES and delta != 0 and ping_time > SUSPECTED_DELAY * 1.3):
        delta -= ping_time 
        delta = 0 if delta < 0 else delta

    # Print the time delta if in DEBUG
    if (DEBUG):
        stdout.write(" {}\n".format(delta))
        stdout.flush()

    # Collect binary values
    if delta <= SUSPECTED_DELAY:
        covert_binary_msg += "0"
    else:
        covert_binary_msg += "1"

# Close connection to server
socket.close()

# Translate binary to ASCII 7bit and 8bit
message8bit = binaryDecoder(covert_binary_msg, 8)
message7bit = binaryDecoder(covert_binary_msg, 7)

# Display both translations
print(f"{covert_binary_msg}\n")
print(f"8-bit message: {message8bit}")
print(f"7-bit message: {message7bit}")