import sys
import getopt

def encode(key,myInput):
        i = 0
        output = ""
        for n in myInput:
                if ord(n) >= 65 and ord(n) <= 90: #Upper Case
                        output += chr((((ord(n)-65) + (ord(key[i])-97))%26)+65)
                        i = (i + 1)%len(key)
                elif ord(n) >= 97 and ord(n) <= 122: #Lower Case
                        output += chr((((ord(n)-97) + (ord(key[i])-97))%26)+97)
                        i = (i + 1)%len(key)
                else:
                        output += n
        return output

def decode(key,myInput):
        i = 0
        output = ""
        for n in myInput:
                if ord(n) >= 65 and ord(n) <= 90: #Upper Case
                        output += chr((((ord(n)-65) - (ord(key[i])-97))%26)+65)
                        i = (i + 1)%len(key)
                elif ord(n) >= 97 and ord(n) <= 122: #Lower Case
                        output += chr((((ord(n)-97) - (ord(key[i])-97))%26)+97)
                        i = (i + 1)%len(key)
                else:
                        output += n
        return output

## main ##
argv = sys.argv[1:]

try:
        opts , args = getopt.getopt(argv, "e:d:")

        if opts[0][0] == '-e':
                key = opts[0][1].lower().replace(" ", "")
                #print(f'key = {key}')
                while(1):
                        print(encode(key,input()))
                
        
        if opts[0][0] == '-d':
                key = opts[0][1].lower().replace(" ", "")
                #print(f'key = {key}')
                while(1):
                        print(decode(key,input()))

except:
        print("Usage: py vigenere.py <-e/-d> <key>")
        exit()
