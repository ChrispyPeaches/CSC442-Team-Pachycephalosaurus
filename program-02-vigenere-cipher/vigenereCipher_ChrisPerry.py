import sys

key = ""
mode = ""
givenInput = ""
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
inputIsStdInOut = False

def encrypt(plainText):
    cipher = ""
    for i in range(len(plainText)):
        if (not plainText[i].isalpha()):
            cipher += plainText[i]
            continue
        ptIndex = alphabet.index(plainText[i].upper())
        keyIndex = alphabet.index(key[i % len(key)].upper())
        tmpCipher = alphabet[( ptIndex + keyIndex ) % 26]
        cipher += tmpCipher.lower() if plainText[i].islower() else tmpCipher
    return cipher

def decrypt(cipher):
    plainText = ""
    for i in range(len(cipher)):
        if (not cipher[i].isalpha()):
            plainText += cipher[i]
            continue
        cIndex = alphabet.index(cipher[i].upper())
        keyIndex = alphabet.index(key[i % len(key)].upper())
        tmpPlainText = alphabet[(26+cIndex-keyIndex) % 26]
        plainText += tmpPlainText.lower() if cipher[i].islower() else tmpPlainText
    return plainText

# Process Message
def processMessage():
    givenInput = ""
    if (not (sys.stdin.isatty())):
        inputIsStdInOut = True
        # If input was a CLI argument
        for line in sys.stdin:
            # Trim line of unneccessary whitespace etc.
            givenInput += line.strip()
            givenInput += "\n" if line.find("\n") == -1 else ""
    else:
        inputIsStdInOut = False
        # If input was not a CLI argument
        givenInput = input()
        givenInput = givenInput.strip()
    return givenInput

def handleOutput():
    if (mode == "encode"):
        print(encrypt(processMessage()))
    elif (mode == "decode"):
        print(decrypt(processMessage()))

def mainloop():
    handleOutput()
    # If input was not an argument, ask for input again
    if (not inputIsStdInOut):
        mainloop()

####################
####    MAIN    ####
####################
# Process arguments
i = 1
while (i < len(sys.argv)):
    currArg = sys.argv[i]
    if (currArg.startswith('-')):
        if (currArg[1:len(currArg)] == 'e'):
            mode = "encode"
        elif (currArg[1:len(currArg)] == 'd'):
            mode = "decode"
    # Handle key
    else:
        key = str(currArg)
        # Handle message with spaces
        if (key.find('"') == 1):
            while True:
                key += sys.argv[i + 1]
                i += 1
                if (sys.argv[i].find('"' == 1)):
                    break
        key = key.replace('"', '')
        key = key.replace(" ", '')
        # Handle invalid message
        if (not key.isalpha()):
            print("Invalid input")
            exit()
    i+=1

mainloop()

