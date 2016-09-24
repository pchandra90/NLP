Problem statement:

Identify Question Type: Given a question, the aim is to identify the category it belongs to. 
The four categories to handle for this assignment are : Who, What, When, Affirmation.

Label any sentence that does not fall in any of the above four as "Unknown" type

Example:
1. What is your name? Type: What
2. When is the show happening? Type: When
3. Is there a cab available for airport? Type: Affirmation
There are ambiguous cases to handle as well like:
What time does the train leave(this looks like a what question but is actually a When type)

*****************************************************************************************

Required package to run NLP_question_type.py: python and NLTK

*****************************************************************************************
When NLP_question_type.py runs, it ask for file name in .txt format. eg. question_type.txt
Input file should contain all questions seprated by punctuation marks.

Sample question_type.txt is attched. 

NLP_question_type.ipynb file contains code and ouput for question_type.txt file. 
