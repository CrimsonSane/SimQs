""" 
Usage by calling program: 
   import InputValidation as iv 

Do not change anything in this file! 

The message is always displayed. 
If a prompt does not exist, the user enters data on the same line as the message.
If a prompt does exist, the message is displayed and then the prompt is displayed on the next line.

Sample usage: 
    import InputValidation as iv 

    x = iv.get_integer("Enter an integer: ")                # no prompt character
    y = iv.get_integer("Enter another integer: ", ">")      # the prompt character is >
    print ("The integers are:", x, "and", y)

Sample output: 
    Enter an integer: 4
    Enter another integer:
    > 5
    The integers are: 4 and 5
"""

def get_integer(message, prompt="none"):
    while True:
        display_prompt(message, prompt)
        try:            
            newValue = int(input())
            return newValue
        except ValueError:
            print('Error: non-numeric value entered')

def get_float(message, prompt="none"):
    while True:
        display_prompt(message, prompt)
        try:
            newValue = float(input())
            return newValue
        except ValueError:
            print('Error: non-numeric value entered')
    
def get_string(message, prompt="none"):
    while True:
        display_prompt(message, prompt)
        newValue = input()
        if newValue and newValue.strip():
            return newValue
        else:
            print('Error: no data entered')
            
def get_yes_or_no(message, prompt="none"):
    while True:
        new_value = get_string(message, prompt)
        new_value = new_value.lower()
        if new_value == "y" or new_value == "yes":
            return True
        if new_value == "n" or new_value == "no":
            return False
        print('Error: invalid value entered') 

def display_prompt(message, prompt):
        print(message, end="")
        if prompt != "none":
            print ("\n" + prompt + " ", end="")

#==========================================================================
#sample execution of the functions
#x = get_integer("Enter an integer: ")            # no prompt character
#y = get_integer("Enter another integer: ", ">")  # the prompt character is >
#print ("The integers are:", x, "and", y)