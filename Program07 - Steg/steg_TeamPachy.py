from sys import argv, stdout, stderr
from enum import Enum
import threading

# The mode the program will use for staggering
class Mode(Enum):
    Bit = 0
    Byte = 1

# The method the program will use for staggering
class Method(Enum):
    Store = 0
    Retrieve = 1

# The method the program will use for storing or retrieving data
class DataStoreMethod(Enum):
    LeftToRight = 0
    RightToLeft = 1

# The method the program will use for staggering
global METHOD

# The mode the program will use for staggering
global MODE

# The offset from the beginning of the file
global OFFSET

# The interval between bytes
global INTERVAL

# File in which we are hiding or retrieving our data
global WRAPPER_FILE

# File where our hidden data is stored (for store method only)
global HIDDEN_FILE

# How the hidden data is stored or retrieved
global DATA_STORE_METHOD

# Value designating hidden file's EOF
global SENTINAL_VALUE

# Designates whether to brute force interval 
# and what value to brute force it up to
#   0 -> Don't brute force
# > 0 -> brute force up to this value
global INTERVAL_BRUTE_FORCE_UPPER_LIMIT

# Default/Initial values
DEBUG = True
INTERVAL = 1
OFFSET = 0
WRAPPER_FILE = None
HIDDEN_FILE = None
DATA_STORE_METHOD = DataStoreMethod.LeftToRight
INTERVAL_BRUTE_FORCE_UPPER_LIMIT = 128
SENTINAL_VALUE = bytearray.fromhex("00 FF 00 00 FF 00")

# Offset
OFFSET_BRUTE_FORCE_LIMIT = 128
OFFSET_INCREMENT_BY_POWERS = True
OFFSET_INCREMENT_BY_POWERS_VALUE = 2
OFFSET_INCREMENT_VALUE = 1


# Custom increment function for bruteforcing interval
# Param: i - integer to increment
# Returns: i with custom incrementation applied
def interval_incrementer(i :int):
    i = i * 2
    return i

def offset_incrementer(i :int):
    if (i == 0):
        i = 1
    if (OFFSET_INCREMENT_BY_POWERS == True):
        i = i * OFFSET_INCREMENT_BY_POWERS_VALUE
        return i
    i = i + OFFSET_INCREMENT_VALUE
    return i

# Process command line arguments and stores them in global variables
def processInput():
    # Make global variables accessible to the function
    global METHOD
    global MODE
    global OFFSET
    global INTERVAL
    global WRAPPER_FILE
    global HIDDEN_FILE
    inMsg = argv
    try:
        for (i, arg) in enumerate(inMsg):
            if(arg.startswith('-')):
                if(arg.startswith('-s')):
                    METHOD = Method.Store
                    continue
                elif(arg.startswith('-r')):
                    METHOD = Method.Retrieve
                    continue
                elif(arg.startswith('-b')):
                    MODE = Mode.Bit
                    continue
                elif(arg.startswith('-B')):
                    MODE = Mode.Byte
                    continue
                elif(arg.startswith('-o')):
                    OFFSET = int(inMsg[i][2:])
                    continue
                elif(arg.startswith('-i')):
                    INTERVAL = int(inMsg[i][2:])
                    continue
                elif(arg.startswith('-w')):
                    WRAPPER_FILE = str(f"{inMsg[i][2:]}")
                    continue
                elif(arg.startswith('-h')):
                    HIDDEN_FILE = str(f"{inMsg[i][2:]}")
                    continue

        if(METHOD == None or MODE == None or WRAPPER_FILE == None):
            raise Exception("Method, mode, and wrapper file arguments are required.")
        elif(METHOD == Method.Store and HIDDEN_FILE == None):
            raise Exception("If method is store, you must specify a hidden file.")
        
        return
    except Exception as e:
        
        raise Exception(f"Invalid Parameters. {e}")

# Decode data from wrapper file
# Param: wrapperContents - bytearray of wrapper file contents
# Returns: hiddenContents retrieved from the wrapperFile
def decodeData(wrapperContents: bytearray, offset: int, interval: int):
    # Make global variables accessible to the function
    global MODE
    global SENTINAL_VALUE
    # The hidden data
    hiddenContents = bytearray()
    # Buffer for tracking if the sentinal value is found
    sentinalBuffer = bytearray()

    try:
        # Retrieve data in Bit mode
        if (MODE == Mode.Bit):
            while(offset < (len(wrapperContents) - (len(SENTINAL_VALUE) + 7 * interval))):
                # Parse current byte
                b = 0b0
                for j in range(0, 8):
                    b |= (wrapperContents[offset] & 0b00000001)
                    if (j < 7):
                        b <<= 0b1
                        offset += interval
                
                # Check for sentinal value & update buffer
                if b == SENTINAL_VALUE[len(sentinalBuffer)]:
                    sentinalBuffer.append(b)
                    if len(sentinalBuffer) == len(SENTINAL_VALUE):
                        break
                else:
                    sentinalBuffer = bytearray()
                
                # Append hidden contents to output file
                hiddenContents.append(b)
                offset += interval

        # Retrieve data in Byte mode
        elif (MODE == Mode.Byte):
            while(offset < len(wrapperContents)):
                # Parse current byte
                b = wrapperContents[offset]

                # Check for sentinal value & update buffer
                if b == SENTINAL_VALUE[len(sentinalBuffer)]:
                    sentinalBuffer.append(b)
                    if (len(sentinalBuffer) == len(SENTINAL_VALUE)):
                        break
                else:
                    sentinalBuffer = bytearray()

                # Append hidden contents to output file
                hiddenContents.append(b)
                offset += interval

        # Remove the sentinal data from the retrieved hidden data
        for i in range(len(sentinalBuffer) - 1):
            hiddenContents.pop()

        # If storing data RightToLeft, reverse data retrieved
        if (DATA_STORE_METHOD == DataStoreMethod.RightToLeft):
            hiddenContents.reverse()
        
        # Check if sentinal value was found, if not return empty bytearray
        if(len(sentinalBuffer) != len(SENTINAL_VALUE)):
            hiddenContents = bytearray()
        return hiddenContents
    
    except Exception as e:
        raise Exception("Failed decoding wrapper contents.\n" +
                        f"Inner Exception:\n{e}" )    

# Store data in wrapper file
# Param: hiddenContents - bytearray of hidden data to store
# Param: wrapperContents - bytearray of wrapper file contents to hide data in
# Returns: wrapperContents with the hiddenContent stored inside
def encodeData(hiddenContents: bytearray, wrapperContents: bytearray):
    # Make global variables accessible to the function
    global MODE
    global OFFSET
    global INTERVAL
    global SENTINAL_VALUE

    # Copy offset so it's reusable
    offset = OFFSET

    try:
        # If storing data RightToLeft, reverse data to be hidden
        if (DATA_STORE_METHOD == DataStoreMethod.RightToLeft):
            hiddenContents.reverse()

        # Store data in Bit mode
        if (MODE == Mode.Bit):
            # Store data to be hidden
            i = 0
            while (i < len(hiddenContents)):
                for j in range(0, 8):
                    wrapperContents[offset] &= 0b11111110
                    wrapperContents[offset] |= ((hiddenContents[i] & 0b10000000) >> 7)
                    hiddenContents[i] = (hiddenContents[i] << 1) & (2 ** 8 - 1)
                    offset += INTERVAL
                i += 1
            
            # Store sentinal data
            i = 0
            while (i < len(SENTINAL_VALUE)):
                for j in range(0, 8):
                    wrapperContents[offset] &= 0b11111110
                    wrapperContents[offset] |= ((SENTINAL_VALUE[i] & 0b10000000) >> 7)
                    SENTINAL_VALUE[i] = (SENTINAL_VALUE[i] << 1) & (2 ** 8 - 1)
                    offset += INTERVAL
                
                i += 1

        # Store data in Byte mode
        elif (MODE == Mode.Byte):
            # Store data to be hidden
            i = 0
            while (i < len(hiddenContents)):
                wrapperContents[offset] = hiddenContents[i]
                offset += INTERVAL
                i += 1

            # Store sentinal data
            i = 0
            while (i < len(SENTINAL_VALUE)):
                wrapperContents[offset] = SENTINAL_VALUE[i]
                offset += INTERVAL
                i += 1

        return wrapperContents
    
    except Exception as e:
        raise Exception("Failed hiding contents in wrapper.\n" +
                        f"Inner Exception:\n{e}" ) 

# Read data from given file
# Param: filePath - path to file to read from
# Returns: bytearray of file contents
def readData(filePath: str):
    fileContents = bytearray()
    try:
        with open(filePath, 'rb') as file:
            fileContents = bytearray(file.read())
        return fileContents
    except Exception as e:
        raise Exception("Failed reading {filePath}\n" +
                        f"Inner Exception:\n{e}")
    
# Write given data to stdout
# Param: filePath - path to file to write to
# Param: fileContents - bytearray of data to write to file
def writeData(fileContents: bytearray, offset: int, interval: int):
    try:
        with open(f"output_{WRAPPER_FILE}_{Mode(MODE).name}_i={interval}_o={offset}", "w") as file:
            file.buffer.write(bytes(fileContents))
    except Exception as e:
        raise Exception("Error writing hidden data to file.\n" +
                        f"Inner Exception:\n{e}" )

def runRetrieve(wrapperContents: bytearray, offset: int, interval: int):
    # Retrieve hidden data from wrapper data
    hiddenContents = decodeData(wrapperContents, offset, interval)

    # If hidden data was found, write it to file
    if len(hiddenContents) != 0:
        # Write hidden data to stdout
        writeData(hiddenContents, offset, interval)
    
    if (DEBUG):
        stderr.write(f"Finished Thread: with\n\tInterval:{interval}\n\tOffset:{offset}\n")

try:
    # Process command line arguments
    processInput()

    # Extract data from wrapper file
    wrapperContents = readData(WRAPPER_FILE)

    # Store the data in the wrapper file
    if (METHOD == Method.Store):
        # Extract the data from the hidden file.
        hiddenContents = readData(HIDDEN_FILE)
        
        # Hide the data inside of the wrapper data
        wrapperContents = encodeData(hiddenContents, wrapperContents)

        # Write the wrapper data to stdout
        writeData(wrapperContents, OFFSET, INTERVAL)

    # Retrieve the data from the wrapper file
    # Always run it once, then if brute force is enabled, 
    # run it until reaching upper limit
    elif (METHOD == Method.Retrieve):
        INITAL_OFFSET = OFFSET
        # If bruteforce is enabled
        if (INTERVAL_BRUTE_FORCE_UPPER_LIMIT != 0):
            # Brute force the interval value
            while(INTERVAL <= INTERVAL_BRUTE_FORCE_UPPER_LIMIT):
                while (OFFSET <= OFFSET_BRUTE_FORCE_LIMIT):
                    # Run the retrieve function using threading
                    t = threading.Thread(target=runRetrieve, args=(wrapperContents, OFFSET, INTERVAL))
                    if (DEBUG):
                        stderr.write(f"Started Thread:\n\tInterval:{INTERVAL}\n\tOffset:{OFFSET}\n")
                    # Start the thread
                    t.start()

                    OFFSET = offset_incrementer(OFFSET)

                # Increment interval value using custom incrementer
                OFFSET = INITAL_OFFSET
                INTERVAL = interval_incrementer(INTERVAL)

        # If brute force is not enabled, only run once
        else:
            # Run the retrieve function once
            runRetrieve(wrapperContents, OFFSET, INTERVAL)

# Print error message to stdout and explain the program's usage if error occurs
# if DEBUG mode is enabled
except Exception as e:
    if (DEBUG):
        stderr.write(
            f"Exception: {e}\n" +
            "Usage:\n" + 
            "python Steg.py -(sr) -(bB) -o<val> [-i<val>] -w<val> [-h<val>]\n" + 
            " -s\tstore\n" +
            " -r\tretrieve\n" +
            " -b\tbit mode\n" +
            " -B\tbyte mode\n" +
            " -o\tset offset to <val> (default is 0)\n" +
            " -i\tset interval to <val> (default is 1)\n" +
            " -w\tset wrapper file to <val>\n" +
            " -h\tset hidden file to <val>\n")