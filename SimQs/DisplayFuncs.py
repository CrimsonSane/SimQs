import GLOBAL_CONSTS as CONST

# Start menu
def display_start_menu():
    print("\n\n\n")
    print("-"*CONST.SPLIT_AMT)
    print("Welcome to SimQs")
    print()
    print("(A) Select a quiz")
    print()
    print("(Q) Quit")
    print()
    print("-"*CONST.SPLIT_AMT)


# Selection menu
def display_selection_menu(quizes):
    print("\n\n\n")
    print("-"*CONST.SPLIT_AMT)
                
    # Display all possible quizes
    for quiz_select in range(len(quizes)):
        
        # if selection number is less than the max alphabet limit
        if quiz_select < len(CONST.NUM_TO_ALPHA):
            print("(" + CONST.NUM_TO_ALPHA[quiz_select] + ") " + quizes[quiz_select][0])
            print()
                
    # Display a message if there are no quizes
    if len(quizes) == 0:
        print("Either an error has occured with the quizes or there are no quizes in the quiz folder: " + CONST.QUIZES_DIR )
        print()
                
    print("(Q) Back")
    print()
    print("-"*CONST.SPLIT_AMT)


# Display quiz question
def display_question(current_question, quiz_nme, quiz_obj, current_question_nbr, answr_result):
    results = quiz_obj.get_results()
    
    print("\n\n\n")
    print("----- " + quiz_nme + " -----" + str(current_question_nbr + 1) + " / " + str(len(quiz_obj.get_questions())) + " -----")
    print()
    print(current_question.get_question())
    print()
    
    # Change to specific answer type
    if current_question.get_answer_type() == "MC":
        print("Choose the correct answer:")
        
        for answer_index in range(len(current_question.get_answers())):
            # if answer index is less than max alphabet limit
            if answer_index < len(CONST.NUM_TO_ALPHA):
                # Check if matches result
                if CONST.NUM_TO_ALPHA[answer_index] == answr_result:
                    # Selected
                    print("(" + CONST.NUM_TO_ALPHA[answer_index] + ") " + str(current_question.get_answers()[answer_index]))
                else:
                    # Unselected
                    print(" " + CONST.NUM_TO_ALPHA[answer_index] + "  " + str(current_question.get_answers()[answer_index]))
                print()
    
    elif current_question.get_answer_type() == "TF":
        print("True or false?")
        
        for answer in ["T", "F"]:
            if answer == answr_result:
                print("(" + answer + ") ")
            else:
                print(" " + answer + "  ")
            print()
    
    print(CONST.QUIT + " to quit, " + CONST.FINISH + " to finish | back: " + CONST.BACK + " next: " + CONST.NEXT)
    print("-"*CONST.SPLIT_AMT)


# display report
def display_report(reprt, questions, quiz_obj):
    # (correct_answers, percnt_correct, percnt_wrong)
    cor_answers, prct_corct, prct_wrng = reprt
    
    print("\n\n\n")
    print("-"*CONST.SPLIT_AMT)
    
    # Display the percentages here
    print("{:.2f}% Correct".format(prct_corct * 100))
    print("{:.2f}% Wrong".format(prct_wrng * 100))
    print()
    
    ROW_ORDER = ["Question #: ", "Your answer: ", "The correct answer: ", "* / X: "]
    
    for row in ROW_ORDER:
        print(row, end=" ")
    print()
    
    # Display which question were correct
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
            print(question_num_col + your_answer_col + cor_answer_col + star_col)
        else:
            print(question_num_col + your_answer_col + cor_answer_col + x_col)
    
    print()
    print("Type " + CONST.OUTPUT + " to output full detailed report to a file, " + CONST.PLAY_AGAIN +" to play again or " + CONST.QUIT + " to quit")
    print()
    print("-"*CONST.SPLIT_AMT)


# 