# SimQs
A simple quizzing system made in Python. SimQs stands for Simple Quizzing system and it is command line quiz interface that uses JSON to format quizzes. This project is for my final project assignment in a problem solving class I'm in. Though it is my final project expect more updates and features to this program and possibly an improved version of this program.

[Go here for changelog](/CHANGELOG.md)

# Installation:
1. Install Python on your OS.
2. Clone this repository.
3. Open up command prompt or terminal.
4. Using the ```cd``` command on the terminal, go to the file location of the cloned repository. You should navigate to the folder that contains main.py.
5. In the terminal type: ```python3 main.py```

# Configuration:
To create a quiz, you need to create a JSON file in the Quizes folder. The formatting for this JSON file is very specific, but this part should be able to guide you to the very basics of the formatting.


## Creating a question
To create a question the file starts with a "questions" entry to signify the start of the list:
```
{"questions":
 [

 ]
}
```
The placement of the brackets don't matter as long as they are in the correct order. ***entry names should be all lowercase.***

***NOTE:*** Curly brackets ```{}``` indicate objects in JSON and square brackets ```[]``` indicate lists in JSON.


Here is what a single questions looks like:
```
{"questions":
 [
  {"question":"Example question?",
   "answer type":"MC",
   "correct answer":"C",
   "possible answers":["test 1",
                       "test 2",
                       "test 3",
                       "test 4"]
  }
 ]
}
```
The order for entries such as "question" and "answer type" doesn't matter as long as they are separated by commas. Notice how the "possible answers" entry has square brackets indicating another list of values separated by commas.


## Multiple questions:
For multiple questions you type the same formatting as you would with creatting one question, the only difference is that it is separated by commas.

Example:
```
{"questions":
 [
  {"question":"Example question 1?",
   "answer type":"MC",
   "correct answer":"C",
   "possible answers":["test 1",
                       "test 2",
                       "test 3",
                       "test 4"]
  }, 
  
  {"question":"Example question 2?",
   "answer type":"TF",
   "correct answer":"T",
   "possible answers":["T", "F"]
  }
 ]
}
```


## Question:
Question indicates the question that will be shown to the user.


## Answer types:
There are currently two answer types at the moment: multiple choice (MC) and true or false (TF). More are likely to be added.


## Correct answer and possible answers:
### For multiple choice:
Correct answer must be a letter value that matches the list of possible answers. The program only goes from A to J so make sure there aren't too many possible answers.

### For true/false:
Correct answer must be either t or f. You aren't required to put "T" and "F" in possible answers, you need **at least one possible answer**.


## Problems:
One of the problems with this method of creating a quiz is the how tedious it is to format multi lined questions or answers.
Heres an example of that on the formatting quiz JSON file:
```
...
"{\n     \"questions\":\n     [\n      {\"question\":\"example question?\"\n       \"correct answer\":\"c\"\n       \"answer type\":\"Mc\"\n       \"possible answers\":[\n         \"this answer\",\n         \"or this answer\",\n         \"or even this answer\"]\n      }\n     ]\n    }",
...
```
# Operating instructions:
The program should tell you what can enter to move to different menus or to do different actions.

## Basic break down:
- "Q" to quit or go back
- "A" to "J" to select quiz or answer
- "S" to submit quiz
- ">" to go to next question
- "<" to go back a question
- "O" to output a file on report menu
- "P" to play again on report file

# License:
This software is under the [MIT license](/LICENSE)

