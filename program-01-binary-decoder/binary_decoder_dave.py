from sys import stdin

def get_octets(bit_string, size=8):   
    """
    Returns a list of all the octet (or size-length groups) of a bit string

    keyword arguments
    bit_string -- a binary string
    size -- group length, e.g. 8 for octets (bytes)
    """
    if len(bit_string) % size != 0:
        return

    octets = [bit_string[i:i+size] for i in range(0, len(bit_string), size)]
    
    return(octets) 

def reverse_string(string):
    reversed_string = ""
    counter = len(string)-1
    while counter != -1:
        reversed_string += string[counter]
        counter -= 1
    return(reversed_string)

def binary_to_decimal(number):
    if type(number) == type(1):
        number = str(number)
    number = reverse_string(number)
    result = 0
    exponent = 0
    for digit in number:
        if digit == "1":
            result += pow(2, exponent)
        exponent += 1
    return(result)

for line in stdin:
    line = line.strip()

size = 7 if len(line) % 7 == 0 else 8

octets = get_octets(line, size)
for octet in octets:
    decimal_equivalent = binary_to_decimal(octet)
    print(chr(decimal_equivalent), end = "")
print()
