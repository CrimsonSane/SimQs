# Alex Herron
# Date: 5/1/2022
# Class: CIS 131
# Assignment: Final Project: SimQs (Simple Quizing System)

import os
import json
import random
import datetime

import InputValidation as inpt_val
import AddnInptVal as add_inpt_val

import GLOBAL_CONSTS as CONST
import DisplayFuncs as display
import isInvalid as invalid

def main():
    running = True
    menu = "START_MENU"
    quizes = []
    current_quiz = None
    quiz_questions = None
    
    while running:
        # Switching to different menus
        match menu:
            # The starting page of the program
            case "START_MENU":
                # Display start menu
                display.display_start_menu()
                
                # Input
                selection = get_valid_strt_mnu_selection()
                
                # Execute command
                menu = execute_strt_mnu_cmd(selection)
                
            # Select a avaliable quiz
            case "SELECTION_MENU":
                # Get quizes
                quizes = get_quizes()
                
                # Display selction menu
                display.display_selection_menu(quizes)
                
                # Input
                selection = get_valid_quiz_sel_mnu_selection(quizes)
                
                # Execute command
                current_quiz, menu = execute_quiz_sel_mnu_cmd(selection, quizes)
                
            case "QUIZ":
                # Catch any problems that may occur if the user happens to some how unload the current quiz
                if current_quiz == None:
                    print("Current quiz is not set")
                    menu = "SELECTION_MENU"
                
                running_quiz = True
                current_qutn_num = 0
                # Randomize the question order
                quiz_questions = randomize_questions(current_quiz)
                
                while running_quiz:
                    current_question = quiz_questions[current_qutn_num]
                    
                    # Get the question result if there is one
                    answer_result = get_result_frm_q_obj(current_quiz, current_question)
                    
                    # Display current question
                    display.display_question(current_question, current_quiz, current_qutn_num, answer_result)
                    
                    # Gather user input depending on question(S to finish/submit, Q to quit, > to go to the next question, < to go back)
                    # Input
                    selection = get_valid_quiz_plying_selection(current_question)
                    
                    # Execute command
                    def_values = (current_quiz, current_qutn_num, running_quiz, quiz_questions, menu)
                    
                    current_quiz, current_qutn_num, running_quiz, quiz_questions, menu = execute_quiz_mnu_cmd(selection, def_values)
            
            case "REPORT_MENU":
                
                # Process report from current quiz
                report = get_quiz_report(current_quiz)
                
                # Display the report
                display.display_report(report, quiz_questions, current_quiz)
                
                # Give user options to: output to a file, play the quiz again, look at the answered questions or quit to selection menu
                # Input
                selection = get_valid_report_mnu_selection()
                
                # Execute command
                def_values = (current_quiz, quiz_questions, menu)
                
                current_quiz, quiz_questions, menu = execute_report_cmd(selection, def_values, report)
                
            # Quit out of program
            case "QUIT":
                running = False
                
            # Unknown menu
            case _:
                print("Unknown menu:", menu)
                running = False


"""--- GET VALID SELECTIONS ---"""
def get_valid_strt_mnu_selection():
    selection = add_inpt_val.get_letter("> ")
                
    # Invalid selection
    while invalid.is_invalid_start_selection(selection):
        print("Error: Invalid selection, try again")
        selection = add_inpt_val.get_letter("> ")
    
    return selection


def get_valid_quiz_sel_mnu_selection(quizes):
    selection = add_inpt_val.get_letter("> ")
                
    # Invalid selection
    while invalid.is_invalid_quiz_select_selection(selection, quizes):
        print("Error: Invalid selection, try again")
        selection = add_inpt_val.get_letter("> ")
    
    return selection


def get_valid_quiz_plying_selection(curnt_questn):
    selection = add_inpt_val.get_letter("> ")
                    
    # Invalid selection
    while invalid.is_invalid_quiz_command(selection, curnt_questn):
        print("Error: Invalid selection, try again")
        selection = add_inpt_val.get_letter("> ")
    
    return selection


def get_valid_quit_quiz_selection():
    selection = add_inpt_val.get_letter("> ")

    # Invalid selection
    while invalid.is_invalid_quit_quiz_command(selection):
        print("Error: Invalid selection, try again")
        selection = add_inpt_val.get_letter("> ")

    return selection



def get_valid_report_mnu_selection():
    selection = add_inpt_val.get_letter("> ")
                
    # Invalid selection
    while invalid.is_invalid_report_command(selection):
        print("Error: Invalid selection, try again")
        selection = add_inpt_val.get_letter("> ")
    
    return selection
"""--- END ---"""


"""--- EXECUTE MENU CMDS ---"""
def execute_strt_mnu_cmd(selc):
    if selc == "A":
        return "SELECTION_MENU"
    
    elif selc == CONST.QUIT:
        return "QUIT"


def execute_quiz_sel_mnu_cmd(selc, quizes):
    if selc != CONST.QUIT:
        # Changes current quiz and menu
        return (quizes[CONST.NUM_TO_ALPHA.index(selc)], "QUIZ")
    
    elif selc == CONST.QUIT:
        return (None, "START_MENU")


def execute_quiz_mnu_cmd(selc, defaults):
    currnt_quiz, currnt_qutn_num, rnning_quiz, quiz_questns, mnu = defaults
    
    if selc == ">":
        # curnt question num is less than length to go next
        if currnt_qutn_num < len(quiz_questns) - 1:
            currnt_qutn_num += 1
            
    elif selc == "<":
        # curnt question num is less than length to go next
        if currnt_qutn_num > 0:
            currnt_qutn_num -= 1
        
    elif selc == CONST.FINISH:
        mnu = "REPORT_MENU"
        rnning_quiz = False
    
    elif selc == CONST.QUIT:
        print("""
                Select a quiting option:
                    Q: quit WITHOUT saving
                    S: quit WITH saving
                    B: go back to quiz""")
        quit_option = get_valid_quit_quiz_selection()

        if quit_option == "S":
            save_quiz(currnt_quiz, currnt_qutn_num, quiz_questns)
            mnu = "SELECTION_MENU"
            currnt_quiz.set_results({})
            currnt_quiz = None
            quiz_questns = None
            rnning_quiz = False
        
        elif quit_option == CONST.QUIT:
            mnu = "SELECTION_MENU"
            currnt_quiz.set_results({})
            currnt_quiz = None
            quiz_questns = None
            rnning_quiz = False
        
    else:
        currnt_quiz.append_results(quiz_questns[currnt_qutn_num].get_id(), selc)
    
    return (currnt_quiz, currnt_qutn_num, rnning_quiz, quiz_questns, mnu)


def execute_report_cmd(selc, defaults, report):
    currnt_quiz, quiz_questns, mnu = defaults
    
    if selc == CONST.OUTPUT:
        # Output full report to a file
        create_report_file(report, currnt_quiz, quiz_questns)
        print("The report has been created in: " + CONST.QUIZ_REPORT_DIR)
        
        mnu = "SELECTION_MENU"
        currnt_quiz.set_results({})
        currnt_quiz = None
        
    elif selc == CONST.PLAY_AGAIN:
        mnu = "QUIZ"
        currnt_quiz.set_results({})
    
    elif selc == CONST.QUIT:
        continue_quit = inpt_val.get_yes_or_no("Are you sure you want to quit the report? Progress will NOT be saved.(yes/no)", prompt="> ")
        if continue_quit:
            mnu = "SELECTION_MENU"
            currnt_quiz.set_results({})
            currnt_quiz = None
            quiz_questns = None
    
    return (currnt_quiz, quiz_questns, mnu)
"""--- END ---"""

def create_report_file(report, quiz_obj, questions):
    # Create a name of the report file
    now_date = datetime.datetime.now()
    count = 0
    file_name = quiz_obj.get_name() + " Report - " + str(now_date.day) + "-" + str(now_date.day) + "-" + str(now_date.year) + ":" + str(count) +".txt"
    
    while invalid.file_exists(os.path.join(CONST.QUIZ_REPORT_DIR, file_name)):
        count += 1
        file_name = quiz_obj.get_name() + " Report - " + str(now_date.day) + "-" + str(now_date.day) + "-" + str(now_date.year) + ":" + str(count) +".txt"
    
    # Gather the report into a string
    report_string = get_report_string(report, quiz_obj, questions)
    
    # Create directory if it does not exist
    if not invalid.dir_exists(CONST.QUIZ_REPORT_DIR):
        os.mkdir(CONST.QUIZ_REPORT_DIR)
    
    # Create the output file with the string
    with open(os.path.join(CONST.QUIZ_REPORT_DIR, file_name), "w") as file:
        file.write(report_string)


def get_report_string(reprt, quiz_obj, questions):
    report_str = ""
    
    # (correct_answers, percnt_correct, percnt_wrong)
    cor_answers, prct_corct, prct_wrng = reprt
    
    report_title = "-" * 50 + " " + quiz_obj.get_name() + " Report " + "-"*50 + "\n\n"
    report_str += report_title
    
    report_str += "{:.2f}% Correct \n".format(prct_corct * 100)
    report_str += "{:.2f}% Wrong \n".format(prct_wrng * 100)
    
    ROW_ORDER = ["Question #: ", "Your answer: ", "The correct answer: ", "* / X: "]
    
    report_str += "\n"
    
    for row in ROW_ORDER:
        report_str += row + " "
    report_str += "\n"
    
    # Put in which question were correct
    for q_num in range(len(questions)):
        
        results = quiz_obj.get_results()
        your_answer = "N/A"
        
        # If the result exists put in the result
        if results.get(questions[q_num]):
            your_answer = results[questions[q_num]]
        
        # Do formating
        # question number
        q_num_val = "#" + str(q_num + 1)
        qu_nbr_left_margin = (len(ROW_ORDER[0]) - len(q_num_val)) // 2
        qu_nbr_right_margin = len(ROW_ORDER[0]) - qu_nbr_left_margin - len(q_num_val)
        
        question_num_col = " " * qu_nbr_left_margin + q_num_val + " " * qu_nbr_right_margin
        
        # your answer
        yr_anwr_left_margin = (len(ROW_ORDER[1]) - len(str(your_answer))) // 2
        yr_anwr_right_margin = len(ROW_ORDER[1]) - yr_anwr_left_margin - len(str(your_answer))
        
        your_answer_col = " " * yr_anwr_left_margin + str(your_answer) + " " * yr_anwr_right_margin
        
        # correct answer
        cor_answer_val = str(questions[q_num].get_correct_answer())
        cor_anwr_left_margin = (len(ROW_ORDER[2]) - len(cor_answer_val)) // 2
        cor_anwr_right_margin = len(ROW_ORDER[2]) - cor_anwr_left_margin - len(cor_answer_val)
        
        cor_answer_col = " " * cor_anwr_left_margin + cor_answer_val + " " * cor_anwr_right_margin
        
        # star/x
        star_x_left_margin = (len(ROW_ORDER[3]) - 1) // 2
        star_x_right_margin = len(ROW_ORDER[3]) - star_x_left_margin - 1
        
        # Star/x col won't display properly in the middle for some reason.
        # I suspect it has something to to with the right margin for correct answers.
        star_col = " " * star_x_left_margin + "*" + " " * star_x_right_margin
        x_col = " " * star_x_left_margin + "X" + " " * star_x_right_margin
        
        if cor_answers[questions[q_num]]:
            report_str += question_num_col + your_answer_col + cor_answer_col + star_col + "\n"
        else:
            report_str += question_num_col + your_answer_col + cor_answer_col + x_col + "\n"
    
    report_str  += "\n" + "-"*50 + "\n\n" 
    
    # Display each question in the form the user usually sees
    for q_num in range(len(questions)):
        current_question = questions[q_num]
        
        report_str += "\n\n\n"
        report_str += "----- " + quiz_obj.get_name() + " -----" + str(q_num + 1) + " / " + str(len(questions)) + " -----\n\n"
        report_str += current_question.get_question() + "\n\n"
        
        # Multiple choice
        if current_question.get_answer_type() == "MC":
            report_str += "Choose the correct answer:\n"
            
            for answer_index in range(len(current_question.get_answers())):
                # if answer index is less than max alphabet limit
                if answer_index < len(CONST.NUM_TO_ALPHA):
                    selected_result = "N/A"
                    
                    if results.get(current_question):
                        selected_result = results[current_question]
                    
                    # Check if matches result
                    if CONST.NUM_TO_ALPHA[answer_index] == selected_result:
                        # Mark correct
                        if CONST.NUM_TO_ALPHA[answer_index] == current_question.get_correct_answer():
                            report_str += "* "
                        else:
                            report_str += "X "
                        
                        report_str += "(" + CONST.NUM_TO_ALPHA[answer_index] + ") " + str(current_question.get_answers()[answer_index])
                        report_str += "\n"
                        
                    else:
                        # Mark correct
                        if CONST.NUM_TO_ALPHA[answer_index] == current_question.get_correct_answer():
                            report_str += "* "
                        else:
                            report_str += "  "
                        
                        report_str += " " + CONST.NUM_TO_ALPHA[answer_index] + "  " + str(current_question.get_answers()[answer_index])
                        report_str += "\n"
                    report_str += "\n"
        
        elif current_question.get_answer_type() == "TF":
            report_str += "True or false?\n"
            
            selected_result = "N/A"
                    
            if results.get(current_question):
                selected_result = results[current_question]
            
            for answer in ["T", "F"]:
                if answer == selected_result:
                    # Mark correct
                    if answer == current_question.get_correct_answer():
                        report_str += "* "
                    else:
                        report_str += "X "
                    
                    report_str += "(" + answer + ") "
                    report_str += "\n"
                else:
                    # Mark correct
                    if answer == current_question.get_correct_answer():
                        report_str += "* "
                    else:
                        report_str += "  "
                    
                    report_str += " " + answer + "  "
                    report_str += "\n"
                
                report_str += "\n"
    
    return report_str


def get_quiz_report(quiz_obj):
    correct_answers = {}
    percnt_correct = 0
    percnt_wrong = 0
    results = quiz_obj.get_results()
    
    # compare each question with the result and the correct answer
    for question in quiz_obj.get_questions():
        
        # If result exists
        if results.get(question):
            
            # Compare question answer with result
            if question.get_correct_answer() == results[question]:
                correct_answers[question] = True
            else:
                correct_answers[question] = False
        else:
            # Since question hasn't been answered it will be false
            correct_answers[question] = False
    
    # calculate percent right/wrong
    correct_count = count_values(correct_answers, True)
    wrong_count = count_values(correct_answers, False)
    
    percnt_correct = correct_count / len(correct_answers)
    percnt_wrong = wrong_count / len(correct_answers)
    
    return (correct_answers, percnt_correct, percnt_wrong)


def count_values(dictionary, value):
    count = 0
    
    for dict_val in dictionary.values():
        if dict_val == value:
            count += 1
    return count


def get_result_frm_q_obj(curnt_quiz, question):
    current_results = curnt_quiz.get_results()
    
    if current_results.get(question.get_id()):
        return current_results[question.get_id()]
    else:
        return ""


def randomize_questions(quiz):
    temp_questions = quiz.get_questions().copy()
    random_qnas = []
    
    while len(temp_questions) > 0:
        # Chose a random question from temp list
        rand_question = random.choice(temp_questions)
        # Put into list
        random_qnas.append(rand_question)
        # Remove from temp list
        temp_questions.remove(rand_question)
    
    return random_qnas


def get_quizes():
    playable_quizes = []
    
    # If file does not exist create directory
    if not invalid.dir_exists(CONST.QUIZES_DIR):
        os.mkdir(CONST.QUIZES_DIR)
    # List files in directory
    file_names = os.listdir(CONST.QUIZES_DIR)
    
    for file in file_names:
        # Get the file location
        file_location = os.path.join(CONST.QUIZES_DIR, file)
        
        # Open that file
        try:
            with open(file_location, "r") as f:
                try:
                    json_dict = json.load(f)
                    
                    playable_quizes.append(create_quiz(json_dict, file))
                except Exception as error:
                    print("JSON failed to parse quiz:", str(file) + " ERROR: " + str(error))
            
        except IsADirectoryError:
            print("There is a directory inside the quiz folder. The program looks for .json files.")
        except:
            print("Unknown file " + str(file) + " cannot be opened.")
    
    return playable_quizes


def remove_file_ext(file_name):
    splitted_value = file_name.split(".")
    splitted_value.remove(splitted_value[-1])
    
    new_value = "".join(splitted_value)
    return new_value


def create_quiz(quiz_json, file_name):
    # Create quiz
    quiz = Quiz()
    qnas = []
    
    # Remove file extention from name
    quiz_name = remove_file_ext(file_name)
    
    # Give the quiz a name
    quiz.set_name(quiz_name)
    
    # raise error if "questions" key does NOT exist
    if not quiz_json.get("questions"):
        raise Exception("questions entry does not exist in file")
    
    for question_num in range(len(quiz_json["questions"])):
        question = quiz_json["questions"][question_num]
        
        # Validate questions before creating them
        
        validate_question_entry(question, question_num)
        
        ask = str(question["question"])
        
        # Make sure answer type is a valid answer type
        if invalid.is_invalid_answer_type(question["answer type"].upper()):
            raise Exception("Entry 'answer type' is invalid. The answer types are: " + str(CONST.ANSWER_TYPES))
        answer_type = question["answer type"].upper()
        
        # Make sure correct answer is valid data type
        if type(question["correct answer"]) != str:
            raise Exception("Entry 'correct answer' is invalid data type. Make sure it is a string by putting double quotes around it.")
        correct_answer = question["correct answer"].upper()
        
        # Make sure possible answers is valid data type
        if type(question["possible answers"]) != list:
            raise Exception("Entry 'possible answers' is invalid data type. Make sure it is a list by putting square brackets [] around strings separated by commas.")
        # Make sure all values in the list are strings
        if invalid.is_invalid_possible_answrs(question["possible answers"]):
            raise Exception("Entry 'possible answers' has invalid data types inside. Make sure to surround any values (besides the commas) in the list with double quotes.")
        possible_answers = question["possible answers"]
        
        # Make sure correct answer matches with possible answers
        if invalid.is_invalid_answer_correlation(possible_answers, correct_answer, answer_type):
            if answer_type == "MC":
                raise Exception("Entry 'possible answers' and 'correct answer' does not correlate with each other. Make sure the 'correct answer' is a single letter (" + CONST.NUM_TO_ALPHA[0] + " to " + CONST.NUM_TO_ALPHA[-1] + ") to match the order of the possible answers.")
            elif answer_type == "TF":
                raise Exception("Entry 'possible answers' and 'correct answer' does not correlate with each other. 'correct answer' must either be T or F.")
            else:
                raise Exception("This error message will never be displayed, unless you some how got past the answer type validation.")
        
        # Append question into list
        qnas.append(Qna(question_num, ask, answer_type, correct_answer, possible_answers))
    # Set the quiz questions
    quiz.set_questions(qnas)
    return quiz


def validate_question_entry(question_dict, questn_num):
    if not question_dict.get("question"):
        raise Exception("'question' entry does not exist in question #" + str(questn_num + 1))
    if not question_dict.get("answer type"):
        raise Exception("'answer type' entry does not exist in question #" + str(questn_num + 1))
    if not question_dict.get("correct answer"):
        raise Exception("'correct answer' entry does not exist in question #" + str(questn_num + 1))
    if not question_dict.get("possible answers"):
        raise Exception("'possible answers' entry does not exist in question #" + str(questn_num + 1))


def get_questns_id_list(questions_list):
    values = []

    for quest in questions_list:
        values.append(quest.get_id())
    return values


def save_quiz(quiz, current_questn_num, questns):
    if not invalid.dir_exists(CONST.QUIZ_SAVE_DIR):
        os.mkdir(CONST.QUIZ_SAVE_DIR)

    with open(os.path.join(CONST.QUIZ_SAVE_DIR, quiz.get_name()), "w") as sav_f:
        questions = get_questns_id_list(questns)
        results = quiz.get_results()

        values_to_save = {"results": results, "question order": questions, "current question number": current_questn_num}

        sav_f.write(json.dumps(values_to_save))


class Quiz():
    def __init__(self, name="NULL", questions=[], results={}):
        self.__name = name
        self.__questions = questions
        self.__results = results
    
    # Name getter/setter
    def get_name(self):
        return self.__name
    
    def set_name(self, name):
        self.__name = name
    
    # Questions getter/setter
    def get_questions(self):
        return self.__questions
    
    def set_questions(self, questions):
        self.__questions = questions
    
    # Results getter/setter
    def get_results(self):
        return self.__results
    
    def set_results(self, results):
        self.__results = results
    
    def append_results(self, key, value):
        self.__results[key] = value


class Qna():
    def __init__(self, id_=0, question="", awr_type="", cor_answer="", answers=[]):
        self.__id = id_
        self.__question = question
        self.__awr_type = awr_type.upper()
        self.__cor_answer = cor_answer
        self.__answers = answers

    # Id getter/setter
    def get_id(self):
        return self.__id
    
    def set_id(self, id_):
        self.__id = id_

    # Question getter/setter
    def get_question(self):
        return self.__question
    
    def set_question(self, question):
        self.__question = question
    
    # Answer_type getter/setter
    def get_answer_type(self):
        return self.__awr_type
    
    def set_answer_type(self, awr_type):
        self.__awr_type = awr_type.upper()
    
    # Correct_answer getter/setter
    def get_correct_answer(self):
        return self.__cor_answer
    
    def set_correct_answer(self, cor_answer):
        self.__cor_answer = cor_answer
    
    # Answers getter/setter
    def get_answers(self):
        return self.__answers
    
    def set_answers(self, answers):
        self.__answers = answers


if __name__ == "__main__":
    main()
