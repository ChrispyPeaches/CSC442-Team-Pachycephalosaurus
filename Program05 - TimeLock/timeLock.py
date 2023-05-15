import datetime as dt
import hashlib as h
import time as t
import pytz # needed for correcting daylight savings

DEBUG_TIMEDATE = False
DEBUG_SECONDS = False
DEBUG_HASH = False

def epoch_reformat(epoch_str):
    # If the formatting is incorrect or invalid, i.e. (2002 25 69 48 02 100), return error
    try:
        # Split the epoch string into a list
        epoch_split = epoch_str.split()

        # format the list into a datetime object
        epoch_time = dt.datetime(int(epoch_split[0]), int(epoch_split[1]), int(epoch_split[2]), int(epoch_split[3]), int(epoch_split[4]), int(epoch_split[5])).astimezone(pytz.utc)

        # DEBUGGING TIMEDATE
        if (DEBUG_TIMEDATE  == True):
            print(f"Epoch time in UTC is: Year: {epoch_time.year}, Month: {epoch_time.month}, Day: {epoch_time.day}, Hour: {epoch_time.hour}, Minute: {epoch_time.minute}, Second: {epoch_time.second}")

        # return the datetime object
        return epoch_time

    except:
        # error message
        return "Not valid input, provide an valid input formatted (YYYY MM DD HH MM SS)"

def time_elapsed(epoch_time):
    # Retrieves the system's time
    current_time = dt.datetime.now().astimezone(pytz.utc)
    #current_time = dt.datetime(2013, 5, 6, 7, 43, 25).astimezone(pytz.utc) # manually set current time

    # DEBUGGING TIMEDATE
    if (DEBUG_TIMEDATE  == True):
        print(f"Current time in UTC is: Year: {current_time.year}, Month: {current_time.month}, Day: {current_time.day}, Hour: {current_time.hour}, Minute: {current_time.minute}, Second: {current_time.second}")

    # Calculates the time elapsed from epoch_time to current_time (both in UTC)
    time_elapsed = (current_time.replace(tzinfo=pytz.utc) - epoch_time.replace(tzinfo=pytz.utc))

    # Converts time_elapsed to seconds
    time_elapsed_in_seconds = int(time_elapsed.total_seconds())

    # DEBUGGING SECONDS
    if (DEBUG_SECONDS == True):
        print(f"Total seconds elapsed: {time_elapsed_in_seconds}")

    # Returns the total seconds
    return time_elapsed_in_seconds

def time_code(time_elapsed):
    valid_second = time_elapsed // 60 * 60

    # DEBUGGING SECONDS
    if (DEBUG_SECONDS == True):
        print(f"Valid second for code: {valid_second}")

    hash1 = h.md5(str(valid_second).encode()).hexdigest()
    hash2 = h.md5(hash1.encode()).hexdigest()

    if (DEBUG_HASH == True):
        print(f"First Hash: {hash1}")
        print(f"Second Hash: {hash2}")

    return first_two_last_two(hash2)


def first_two_last_two(string):
    reverse_string = string[::-1]

    letters = ''
    numbers = ''

    for char in string:
        if char.isalpha():
            letters += char

    for number in reverse_string:
        if number.isdigit():
            numbers += number

    return letters[0:2] + numbers[0:2]


time_inputed = input()

print(time_code(time_elapsed(epoch_reformat(time_inputed))))
