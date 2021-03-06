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
                display.display_start_menu()
                
                # Input
                selection = add_inpt_val.get_letter("> ")
                
                # Invalid selection
                while invalid.is_invalid_start_selection(selection):
                    print("Error: Invalid selection, try again")
                    selection = add_inpt_val.get_letter("> ")
                
                # Execute command
                if selection == "A":
                    menu = "SELECTION_MENU"
                elif selection == CONST.QUIT:
                    menu =  "QUIT"
                
            # Select a avaliable quiz
            case "SELECTION_MENU":
                # Get quizes
                quizes = get_quizes()
                
                display.display_selection_menu(quizes)
                
                # Input
                selection = add_inpt_val.get_letter("> ")
                
                # Invalid selection
                while invalid.is_invalid_quiz_select_selection(selection, quizes):
                    print("Error: Invalid selection, try again")
                    selection = add_inpt_val.get_letter("> ")
                
                # Execute command
                if selection != CONST.QUIT:
                    current_quiz = quizes[CONST.NUM_TO_ALPHA.index(selection)]
                    menu = "QUIZ"
                elif selection == CONST.QUIT:
                    menu = "START_MENU"
                
            case "QUIZ":
                # Catch any problems that may occur if the user happens to some how unload the current quiz
                if current_quiz == None:
                    print("Current quiz is not set")
                    menu = "SELECTION_MENU"
                
                quiz_name, quiz_obj = current_quiz
                running_quiz = True
                current_qutn_num = 0
                # Randomize the question order
                quiz_questions = randomize_questions(current_quiz)
                
                while running_quiz:
                    current_question = quiz_questions[current_qutn_num]
                    
                    # Get the question result if there is one
                    answer_result = get_result_frm_q_obj(quiz_obj, current_question)
                    
                    # Display current question
                    display.display_question(current_question, quiz_name, quiz_obj, current_qutn_num, answer_result)
                    
                    # Gather user input depending on question(S to finish/submit, Q to quit, > to go to the next question, < to go back)
                    # Input
                    selection = add_inpt_val.get_letter("> ")
                    
                    # Invalid selection
                    while invalid.is_invalid_quiz_command(selection, current_question):
                        print("Error: Invalid selection, try again")
                        selection = add_inpt_val.get_letter("> ")
                    
                    # Execute command
                    if selection == ">":
                        # curnt question num is less than length to go next
                        if current_qutn_num < len(quiz_questions) - 1:
                            current_qutn_num += 1
                    elif selection == "<":
                        # curnt question num is less than length to go next
                        if current_qutn_num > 0:
                            current_qutn_num -= 1
                    elif selection == CONST.FINISH:
                        menu = "REPORT_MENU"
                        running_quiz = False
                    elif selection == CONST.QUIT:
                        continue_quit = inpt_val.get_yes_or_no("Are you sure you want to quit the quiz? Progress will NOT be saved.(yes/no)", prompt="> ")
                        if continue_quit:
                            menu = "SELECTION_MENU"
                            quiz_obj.set_results({})
                            current_quiz = None
                            quiz_questions = None
                            running_quiz = False
                    else:
                        quiz_obj.append_results(current_question, selection)
            
            case "REPORT_MENU":
                quiz_name, quiz_obj = current_quiz
                
                # Process report from current quiz
                report = get_quiz_report(quiz_obj)
                
                # Display the report
                display.display_report(report, quiz_questions, quiz_obj)
                
                # Give user options to: output to a file, play the quiz again, look at the answered questions or quit to selection menu
                # Input
                selection = add_inpt_val.get_letter("> ")
                
                # Invalid selection
                while invalid.is_invalid_report_command(selection):
                    print("Error: Invalid selection, try again")
                    selection = add_inpt_val.get_letter("> ")
                
                # Execute command
                if selection == CONST.OUTPUT:
                    # Output full report to a file
                    create_report_file(report, quiz_obj, quiz_name, quiz_questions)
                    
                    menu = "SELECTION_MENU"
                    quiz_obj.set_results({})
                    current_quiz = None
                elif selection == CONST.PLAY_AGAIN:
                    menu = "QUIZ"
                    quiz_obj.set_results({})
                elif selection == CONST.QUIT:
                    continue_quit = inpt_val.get_yes_or_no("Are you sure you want to quit the report? Progress will NOT be saved.(yes/no)", prompt=">")
                    if continue_quit:
                        menu = "SELECTION_MENU"
                        quiz_obj.set_results({})
                        current_quiz = None
                        quiz_questions = None
                
            # Quit out of program
            case "QUIT":
                running = False
                
            # Unknown menu
            case _:
                print("Unknown menu:", menu)
                running = False


def create_report_file(report, quiz_obj, quiz_nme, questions):
    # Create a name of the report file
    now_date = datetime.datetime.now()
    count = 0
    file_name = quiz_nme + " Report - " + str(now_date.day) + "-" + str(now_date.day) + "-" + str(now_date.year) + ":" + str(count) +".txt"
    
    while invalid.file_exists(os.path.join(CONST.QUIZ_REPORT_DIR, file_name)):
        count += 1
        file_name = quiz_nme + " Report - " + str(now_date.day) + "-" + str(now_date.day) + "-" + str(now_date.year) + ":" + str(count) +".txt"
    
    # Gather the report into a string
    report_string = get_report_string(report, quiz_obj, quiz_nme, questions)
    
    # Create the output file with the string
    with open(os.path.join(CONST.QUIZ_REPORT_DIR, file_name), "w") as file:
        file.write(report_string)


def get_report_string(reprt, quiz_obj, quiz_nme, questions):
    report_str = ""
    
    # (correct_answers, percnt_correct, percnt_wrong)
    cor_answers, prct_corct, prct_wrng = reprt
    
    report_title = "-" * 50 + " " + quiz_nme + " Report " + "-"*50 + "\n\n"
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
        report_str += "----- " + quiz_nme + " -----" + str(q_num + 1) + " / " + str(len(questions)) + " -----\n\n"
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
    
    if current_results.get(question):
        return current_results[question]
    else:
        return ""


def randomize_questions(quiz):
    temp_questions = quiz[1].get_questions().copy()
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
                    
                    playable_quizes.append((file, create_quiz(json_dict)))
                except Exception as error:
                    print("JSON failed to parse quiz:", str(file) + " ERROR: " + str(error))
            
        except IsADirectoryError:
            print("There is a directory inside the quiz folder. The program looks for .json files.")
        except:
            print("Unknown file " + str(file) + " cannot be opened.")
    
    return playable_quizes

def create_quiz(quiz_json):
    # Create quiz
    quiz = Quiz()
    qnas = []
    
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
        qnas.append(Qna(ask, answer_type, correct_answer, possible_answers))
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


class Quiz():
    def __init__(self, questions=[], results={}):
        self.__questions = questions
        self.__results = results
    
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
    def __init__(self, question="", awr_type="", cor_answer="", answers=[]):
        self.__question = question
        self.__awr_type = awr_type.upper()
        self.__cor_answer = cor_answer
        self.__answers = answers
    
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