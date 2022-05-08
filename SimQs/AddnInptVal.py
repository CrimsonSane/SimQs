# Alex Herron
# Date: 3/24/2022
# Addition Input Validation

import InputValidation as inpt_val

SPLIT_AMT = 45

""" is_invalid functions ------>"""

# Returns true if the number has an invalid range
def is_invalid_rng(vlue, rng):
    if vlue > rng[1]:
        print("Error: value is greater than " + str(rng[1]))
        print("-"*SPLIT_AMT)
        return True
    
    if vlue < rng[0]:
        print("Error: value is less than " + str(rng[0]))
        print("-"*SPLIT_AMT)
        return True
    return False


# Returns true if the number has an invalid range and allows a sentinel
def is_invalid_rng_sntl(vlue, rng, stnl):
    if vlue == stnl:
        return False
    
    if vlue > rng[1]:
        print("Error: value is greater than " + str(rng[1]))
        print("-"*SPLIT_AMT)
        return True
    
    if vlue < rng[0]:
        print("Error: value is less than " + str(rng[0]))
        print("-"*SPLIT_AMT)
        return True
    return False


# Returns true if the string is not one letter
def is_invalid_letr(vlue):
    if vlue.isdigit():
        print("Error: value cannot be a number")
        print("-"*SPLIT_AMT)
        return True
    
    if len(vlue) > 1:
        print("Error: value must be a single letter")
        print("-"*SPLIT_AMT)
        return True
    return False


# Returns true if the string has an invalid range, is not one letter and allows a sentinel
def is_invalid_alp_rng_sntl(vlue, rng, stnl):
    if vlue == stnl:
        return False
    
    if vlue.isdigit():
        print("Error: value cannot be a number")
        print("-"*SPLIT_AMT)
        return True
    
    if len(vlue) > 1:
        print("Error: value must be a single letter")
        print("-"*SPLIT_AMT)
        return True
    
    if vlue > rng[1]:
        print("Error: value is greater than " + str(rng[1]))
        print("-"*SPLIT_AMT)
        return True
    
    if vlue < rng[0]:
        print("Error: value is less than " + str(rng[0]))
        print("-"*SPLIT_AMT)
        return True
    return False

""" get_data functions ------>"""

# Returns a single letter command from a range with a sentinel
def get_letter_from_range_sntl(message, alp_range, sntl):
    # Validate tuple range
    validate_alp_tuple_range(alp_range)
    
    value = inpt_val.get_string(message).upper()
    
    while is_invalid_alp_rng_sntl(value, alp_range, sntl):
        value = inpt_val.get_string(message).upper()
    
    return value

# Returns a single letter command
def get_letter(message):
    value = inpt_val.get_string(message).upper()
    
    while is_invalid_letr(value):
        value = inpt_val.get_string(message).upper()
    
    return value

# Returns integer from specific tuple range
def get_int_from_range(message, num_range):
    # Validate tuple range
    validate_tuple_range(num_range)
    
    num = inpt_val.get_integer(message)
    
    while is_invalid_rng(num, num_range):
        num = inpt_val.get_integer(message)
    
    return num


# Returns integer from specific tuple range and allows a sentinel
def get_int_from_range_sntl(message, num_range, sntl):
    # Validate tuple range
    validate_tuple_range(num_range)
    
    num = inpt_val.get_integer(message)
    
    while is_invalid_rng_sntl(num, num_range, sntl):
        num = inpt_val.get_integer(message)
    
    return num


""" other validation functions ------>"""

def validate_tuple_range(tuple_rng):
    if type(tuple_rng) != tuple:
        raise ValueError("Range is not a tuple.")
    elif len(tuple_rng) != 2:
        raise ValueError("Tuple must contain 2 values.")
    
    for val in tuple_rng:
        # Return a error if the value is not a float or a int
        if type(val) != float and type(val) != int:
            raise ValueError("Value: " + str(val) + " is type: " + str(type(val)) + ", not a int or float")

def validate_alp_tuple_range(alp_tuple_rng):
    if type(alp_tuple_rng) != tuple:
        raise ValueError("Range is not a tuple.")
    elif len(alp_tuple_rng) != 2:
        raise ValueError("Tuple must contain 2 values.")
    
    for val in alp_tuple_rng:
        # Return a error if the value is not a string
        if type(val) != str:
            raise ValueError("Value: " + str(val) + " is type: " + str(type(val)) + ", not a str")
        # Return a error if the length is greater than 1
        if len(val) > 1:
            raise ValueError("Value: " + str(val) + " is greater than 1")
    