import sys

alphabet = "abcdefghijklmnopqrstuvwxyz"
keyshift = 0
text = input()
args = sys.argv[2:len(sys.argv)]
key = ''.join(args).lower()

# Encrypt
if sys.argv[1] == '-e':
    encryptedText = ""
    for i in range(len(text)):
        if text[i].lower() not in alphabet:
            encryptedText += text[i]
            keyshift += 1   
        else:
            
            i1 = alphabet.index(text[i].lower())  

            try:
                i2 = alphabet.index(key[i-keyshift])
            except:
                key += key
                i2 = alphabet.index(key[i-keyshift])

            try:
                if text[i].islower():
                    encryptedText += alphabet[i1+i2]
                else:
                    encryptedText += alphabet[i1+i2].upper()
            except:
                if text[i].islower():
                    encryptedText += alphabet[(i1+i2)%26]
                else:
                    encryptedText += alphabet[(i1+i2)%26].upper()
    
    print("Encrypted message = " + encryptedText)

      
#Decrypt
else:
    decryptedText = ""
    for i in range(len(text)):
        if text[i].lower() not in alphabet:
            decryptedText += text[i]
            keyshift += 1   
        else:
            
            i1 = alphabet.index(text[i].lower())  

            try:
                i2 = alphabet.index(key[i-keyshift])
            except:
                key += key
                i2 = alphabet.index(key[i-keyshift])

            try:
                if text[i].islower():
                    decryptedText += alphabet[i1-i2]
                else:
                    decryptedText += alphabet[i1-i2].upper()
            except:
                if text[i].islower():
                    decryptedText += alphabet[(i1-i2)%26]
                else:
                    decryptedText += alphabet[(i1-i2)%26].upper()
    
    print("Decrypted message = " + decryptedText)


