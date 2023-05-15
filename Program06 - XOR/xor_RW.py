import sys

KEYNAME = "k3y" # name of key file (should be in the same directory as this python file)
keyData = bytearray(open(KEYNAME, "rb").read()) # key file as a byte array
msgData = bytearray(sys.stdin.buffer.read()) # input message file as a byte array
outData = [] # list for all output bytes

if(len(keyData) != len(msgData)): # if files are different sizes, notify user
    print("Error: Input and key files are different sizes.")
else:
    for i in range(len(keyData)): # loop through every byte
        byteM = format(msgData[i], '08b') # include leading zeros
        byteK = format(keyData[i], '08b')

        byteO = '' # placeholder for the output bits
        for j in range(0, 8): # compare each bit
            if(byteK[j] == byteM[j]):
                byteO += '0' # inputs are equal, XOR returns 0
            else:
                byteO += '1' # inputs not equal, XOR returns 1
        outData.append(int(byteO, 2)) # add the byte to the output data as an int

sys.stdout.buffer.write(bytearray(outData))
