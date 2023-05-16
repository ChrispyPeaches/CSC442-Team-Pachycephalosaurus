import sys

finalString = ""
for line in sys.stdin:
    # Trim line of unneccessary whitespace etc.
    tmpLine = line.strip()
    # Separate each line into 7 or 8 bit binary groups and concatenate
    # them into a string represeting the decoded message
    if (len(tmpLine) % 7 == 0):
        for i in range(0, len(tmpLine), 7):
            finalString += chr(int(tmpLine[i:i+7], 2))
    else:
        for i in range(0, len(tmpLine), 8):
            finalString += chr(int(tmpLine[i:i+8], 2))
    finalString += "\n" if line.find("\n") == -1 else ""

# print the final string
print(finalString)

