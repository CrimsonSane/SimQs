import os
import GLOBAL_CONSTS as CONST

# Start menu
def is_invalid_start_selection(user_selection):
    # A is start value
    if user_selection == "A":
        return False
    # Quit is for quiting
    if user_selection == CONST.QUIT:
        return False
    return True


# Quiz selection
def is_invalid_quiz_select_selection(user_selection, quizes):
    for quiz_num in range(len(quizes)):
        
        # number must be less than the max alphabet limit
        if quiz_num < len(CONST.NUM_TO_ALPHA):
            if user_selection == CONST.NUM_TO_ALPHA[quiz_num]:
                return False
            
    # Quit is for going back
    if user_selection == CONST.QUIT:
        return False
    return True


# Quiz commands
def is_invalid_quiz_command(user_selection, current_question):
    POSSIBLE_ANSWERS_TF = ("T", "F")
    
    # For MC answer type:
    if current_question.get_answer_type() == "MC":
        for answer_index in range(len(current_question.get_answers())):
            
            # number must be less than the max alphabet limit
            if answer_index < len(CONST.NUM_TO_ALPHA):
                if user_selection == CONST.NUM_TO_ALPHA[answer_index]:
                    return False
    
    # For TF answer type:
    if current_question.get_answer_type() == "TF":
        for answer_index in range(len(POSSIBLE_ANSWERS_TF)):
            if user_selection == POSSIBLE_ANSWERS_TF[answer_index]:
                return False
            
    # Next is going for next question
    if user_selection == CONST.NEXT:
        return False
    
    # Next is going for the question behind the current
    if user_selection == CONST.BACK:
        return False
    
    # Finish is for finishing the quiz
    if user_selection == CONST.FINISH:
        return False
    
    # Quit is for going back
    if user_selection == CONST.QUIT:
        return False
    return True


# Quit quiz commands
def is_invalid_quit_quiz_command(user_selection):
    # Go back to quiz
    if user_selection == "B":
        return False

    # Quit without saving 
    if user_selection == "Q":
        return False

    # Quit with saving
    if user_selection == "S":
        return False
    return True


# Report commands
def is_invalid_report_command(user_selection):
    # Output is output the report to file
    if user_selection == CONST.OUTPUT:
        return False
    # Play again is for playing the quiz again
    if user_selection == CONST.PLAY_AGAIN:
        return False
    # Quit is for going back to selection
    if user_selection == CONST.QUIT:
        return False
    return True


# Checks for invalid datatypes in possible answers
def is_invalid_possible_answrs(pos_answrs):
    for answr in pos_answrs:
        if type(answr) != str: 
            return True
    return False


# Checks if the answer type is valid
def is_invalid_answer_type(answr_type):
    for an_type in CONST.ANSWER_TYPES:
        if answr_type == an_type:
            return False
    return True


# Checks possible answers to correct answer correlation
def is_invalid_answer_correlation(pos_answrs, cor_answr, answer_type):
    # Multiple choice answer type
    if answer_type == "MC":
        for answr_index in range(len(pos_answrs)):
            
            # number must be less than the max alphabet limit
            if answr_index < len(CONST.NUM_TO_ALPHA):
                
                # Is the correct answer a letter that corresponds to possible answers
                if cor_answr == CONST.NUM_TO_ALPHA[answr_index]:
                    return False
    # True/False answer type
    elif answer_type == "TF":
        if cor_answr == "T" or cor_answr == "F":
            return False
    return True


# checks if file exists
def file_exists(file_path):
    try:
        with open(file_path, "r") as f:
            return True
    except:
        return False


# checks if directory exists
def dir_exists(dir_path):
    if os.path.isdir(dir_path):
        return True
    
    return False

