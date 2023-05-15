# use Python 3
import socket
from sys import stdout
from time import time

def decode_binary(covert_binary: str, amount_of_bits: int) -> str:
    """
    returns the plain text string representation of a message in binary. 

    keyword arguments
    covert_binary  -- a string corresponding to a covert message in binary to be decoded
    amount_of_bits -- how big groupings of binary should be, e.g. 8 for bytes
    """
    overt_message = ""
    for x in range(0, len(covert_binary), amount_of_bits):
        # e.g. a byte, hword, word, dword, qword
        binary_term = covert_binary[x : x + amount_of_bits]
        ascii_code = int(f"0b{binary_term}", 2)
        decoded_character = chr(ascii_code)
        overt_message += decoded_character 
        for delimiter in ["EOF", "eof"]:
            if overt_message.endswith(delimiter):
                overt_message.replace(delimiter, "")
                return(overt_message)

# enables debugging output
DEBUG = False
DELAY_THRESHOLD = 0.05

# set the server's IP address and port
ip = "138.47.99.64"
port = 31337

# create the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the server
s.connect((ip, port))

# receive data until EOF
covert_message = ""
data = s.recv(4096).decode()

while (data.rstrip("\n") != "EOF"):
    # output the data
    stdout.write(data)
    stdout.flush()

    # start the "timer", get more data, and end the "timer"
    timer_start = time()
    data = s.recv(4096).decode()
    timer_end = time()

    # calculate the time delta (and output if debugging)
    delta = round(timer_end - timer_start, 3)
    if (DEBUG):
        stdout.write(" {}\n".format(delta))
        stdout.flush()
    
    # construct covert message in binary by adding 
    # bits to covert_message based on the observed delay
    covert_message += "0" if delta <= DELAY_THRESHOLD else "1"

# close the connection to the server
s.close()

# decode the binary message
overt_8_bit = decode_binary(covert_message, 8)
overt_7_bit = decode_binary(covert_message, 7)

print(f"Covert message: {covert_message}")
print(f"Overt message (8-bit): {overt_8_bit}")
print(f"Overt message (7-bit): {overt_7_bit}")
