from sys import argv, stdin
import copy

# use a dictionary to speed up index search time
alphabet = dict()
for index, char in enumerate("abcdefghijklmnopqrstuvwxyz"):
    alphabet[char] = index

mod_value = len("abcdefghijklmnopqrstuvwxyz")

def encode(p, k):
    # if character is not alphabetic, return character as is
    if not p.isalpha():
        return(p)
    
    # get indices
    p_i = alphabet[p.lower()]
    k_i = alphabet[k.lower()]
    c_i = (p_i + k_i) % mod_value
    
    # determine character for cipher text
    if p.islower():
        c = "abcdefghijklmnopqrstuvwxyz"[c_i]
    else:
        c = "abcdefghijklmnopqrstuvwxyz"[c_i].upper()
    return(c)
    
def decode(c, k):
    # if character is not alphabetic, return character as is
    if not c.isalpha():
        return(c)
    
    # get indices
    c_i = alphabet[c.lower()]
    k_i = alphabet[k.lower()]
    p_i = (mod_value + c_i - k_i) % mod_value
    
    # determine character for plain text
    if c.islower():
        p = "abcdefghijklmnopqrstuvwxyz"[p_i]
    else:
        p = "abcdefghijklmnopqrstuvwxyz"[p_i].upper()
    return(p)

def get_space_indices(string):
    indices = []
    for i in range(len(string)):
        if string[i] == " ":
            indices.append(i)
    return(indices)
        
def restore_spaces(encoded, white_space_indices):
    restored = ""
    start = 0
    for i in range(len(white_space_indices)):
        # amount of spaces creates an offset, so to account for
        # the offset, decrease by i (amount of whitespaces thusfar accounted for)
        restored += f"{encoded[start:white_space_indices[i]-i]} "
        start = white_space_indices[i]-i
    # get the rest of the characters that come after 
    # the final space
    restored += encoded[start:]
    return(restored)
            
def pad_key(key, plain_text):
    new_key = copy.copy(key)
    stopping_point = len(plain_text)
    index = 0
    while(len(new_key) < stopping_point):
        new_key += key[index]
        index += 1
        if index >= len(key):
            index = 0
    return(new_key)

# mode and key must be provided        
if len(argv) < 3:
    exit()

# 3. ignore spaces from key
original_key = argv[2].replace(" ", "")

# determine this ahead of time instead of always checking
translate = encode if argv[1] == "-e" else decode

def process(message):
    # 1. get indices of whitespaces
    white_space_indices = get_space_indices(message)
    
    # 2. remove all whitespaces from plain text
    message = message.replace(" ", "")
    
    # 4. if key is shorter than plain text, pad it
    if len(original_key) < len(message):
        key = pad_key(original_key, message)
    else:
        key = copy.copy(original_key)
    
    modified_message = ""
    
    for i in range(len(message)):
        modified_message += translate(message[i], key[i])
    
    modified_message = restore_spaces(modified_message, white_space_indices)
    return(modified_message)

# read from stdin
for line in stdin:
    print(process(line))