import gspread
import pandas as pd
import os
import time
from google.oauth2.service_account import Credentials
from colorama import Fore, Style, Back


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('holidays survey')

# connect Pandas to Google Sheets
# code taken from GitHub user orlagh-sweeney
data = SHEET.worksheet('survey_answers').get_all_values()
headers = data.pop(0)
df = pd.DataFrame(data, columns=headers)
df.head()

# Colorama colours for the terminal
RED = Fore.RED  # red text for error messages
WHITE = Fore.WHITE  # white text for instructions
YELLOW = Fore.YELLOW  # yellow text for questions and inputs
BLUE = Fore.BLUE  # blue text for tables & highlighted text
BACKGROUND = Back.WHITE  # white background for tables
RESET = Style.RESET_ALL  # resets the colours


def clear_screen():
    """
    This function clear the console screen.
    The provided code checks whether the operating system
    is posix (as in Linux or macOS) or not, and runs the
    appropriate command to clear the screen.
    code taken from geeksforgeeks.org
    """
    if os.name == "posix":
        _ = os.system("clear")
    else:
        _ = os.system("cls")


def survey_results():
    """
    This function request the user to choose between different
    options to show the survey results.
    """
    selection = 0
    while selection != 1 and selection != 2:
        try:
            print(WHITE + "Select an option:\n")
            print("1 - Show the results by age group.")
            print("2 - Show the results by gender.\n" + RESET)
            selection = int(input(YELLOW + "Enter your choice: " + RESET))
            if selection != 1 and selection != 2:
                clear_screen()
                print(RED + "Invalid choice, please enter 1 or 2" + RESET)
        except ValueError:
            clear_screen()
            print(RED + "Invalid input, please enter a valid number" + RESET)
    clear_screen()
    if selection == 1:
        clear_screen()
        question_selection(df,groupby_col='age group')
    else:
        clear_screen()
        question_selection(df,groupby_col='gender')


def question_selection(df_raw,groupby_col):
    """
    This function allows the user to choose between the different
    questions displayed in the survey and then show the results in 
    porcentages.
    """
    print(WHITE + "Select a question to show the results:\n")
    headers = SHEET.worksheet('predefined_answers').row_values(1)
    num_of_questions = (len(headers)-2)
    for i, header in enumerate(headers[2:], start=1):
        print(YELLOW + f"{i}. {header}" + RESET)
    user_input = 0
    while user_input < 1 or user_input > num_of_questions:
        try:
            user_input = int(input(YELLOW + "\nEnter your choice: " + RESET))
            if user_input < 1 or user_input > num_of_questions:
                print(RED + "Invalid choice. Please enter a number" +
                            f"between 1 and {num_of_questions}" + RESET)
        except ValueError:
            print(RED + "Invalid input. Please enter a valid number." + RESET)
    
    # display_percentage(df, groupby_col, user_input)
    return user_input
    print(user_input)


def first_selection():
    """
    This function allows users to choose between taking the survey
    and viewing the survey results.
    """
    selection = 0
    while selection != 1 and selection != 2:
        try:
            print(WHITE + "Select an option:\n")
            print("1 - Take the Survey.")
            print("2 - View Survey results.\n" + RESET)
            selection = int(input(YELLOW + "Enter your choice: " + RESET))
            if selection != 1 and selection != 2:
                clear_screen()
                print(RED + "Invalid choice, please enter 1 or 2" + RESET)
        except ValueError:
            clear_screen()
            print(RED + "Invalid input, please enter a valid number" + RESET)
    clear_screen()
    if selection == 1:
        get_survey()
    else:
        survey_results()


user_choices = []  # global variable to store user choices


def display_questions_and_options(column, num_options):
    """
    Display the question and the options that correspond to the column and
    options parameters given.
    """
    global user_choices  # access to the global variable

    data = SHEET.worksheet('predefined_answers').get_all_values()

    question = data[0][column - 1]
    options = [row[column - 1]for row in data[1:]]

    print(YELLOW + question + RESET)
    for i, option in enumerate(options, start=1):
        print(YELLOW + f"{i}. {option}" + RESET)
        if i >= num_options:
            break
    user_input = -1
    while user_input < 1 or user_input > num_options:
        try:
            user_input = int(input(YELLOW + "Enter your choice: " + RESET))
            if user_input < 1 or user_input > num_options:
                print(RED + "Invalid choice. Please enter a number" +
                            f"between 1 and {num_options}" + RESET)
        except ValueError:
            print(RED + "Invalid input. Please enter a valid number." + RESET)

    selected_option = options[user_input - 1]
    print(YELLOW + f"You selected: {selected_option}" + RESET)
    user_choices.append(selected_option)


def get_survey():
    """
    This function iterates over a dictionary with columns as keywords
    and num_options as values to generate all the questions for the
    survey. Then return a list with all the choosen options.
    """
    survey_questions = {
        1: 6,  # question 1 with 6 options
        2: 2,  # question 2 with 2 options
        3: 4,  # question 3 with 4 options
        4: 4,  # question 4 with 4 options
        5: 6,  # question 5 with 6 options
        6: 8,  # question 6 with 8 options
        7: 9,  # question 7 with 9 options
        8: 9,  # question 8 with 9 options
        9: 9,  # question 9 with 9 options
        10: 2,  # question 10 with 2 options
    }

    for column, num_options in survey_questions.items():
        display_questions_and_options(column, num_options)

        time.sleep(2)
        clear_screen()

    completed_survey_options()


def update_survey_answers(data):
    """
    Update the survey_answers worksheet with the data provided by the user.
    """
    print(WHITE + "Updating the survey results...\n" + RESET)
    SHEET.worksheet("survey_answers").append_row(data)
    print(WHITE + "The survey results has been updated\n" + RESET)


def completed_survey_options():
    """
    Displays various options to the user after completing the survey
    and executes the option that the user requests.
    """
    clear_screen()
    print(BLUE + "THANK YOU FOR COMPLETING THE SURVEY." + RESET)
    print(WHITE + "Survey results:")
    for i, choice in enumerate(user_choices):
        print(f"Question {i + 1}. You answer: {choice}" + RESET)
    print(BLUE + "\n1- Not happy with your answwers?.Repeat the survey.")
    print("2- Submit your answers and view survey results.")
    print("3- Submit your answers and exit survey." + RESET)

    user_input = 0

    while user_input < 1 or user_input > 3:
        try:
            user_input = int(input(YELLOW + "Enter your choice: " + RESET))
            if user_input < 1 or user_input > 3:
                print(RED + "Invalid choice. Please enter a number" +
                            "between 1 and 3" + RESET)
        except ValueError:
            print(RED + "Invalid input. Please enter a valid number." + RESET)
    if user_input == 1:
        clear_screen()
        user_choices.clear()
        get_survey()
    elif user_input == 2:
        clear_screen()
        update_survey_answers(user_choices)
        time.sleep(3)
        survey_results()
    elif user_input == 3:
        clear_screen()
        update_survey_answers(user_choices)
        exit()


def welcome():
    """
    Welcome message to start the holiday survey.
    """
    print("""\
    db   db  .d88b.  db      d888888b d8888b.  .d8b.  db    db
    88   88 .8P  Y8. 88        `88'   88  `8D d8' `8b `8b  d8'
    88ooo88 88    88 88         88    88   88 88ooo88  `8bd8'
    88~~~88 88    88 88         88    88   88 88~~~88    88
    88   88 `8b  d8' 88booo.   .88.   88  .8D 88   88    88
    YP   YP  `Y88P'  Y88888P Y888888P Y8888D' YP   YP    YP


    .d8888. db    db d8888b. db    db d88888b db    db
    88'  YP 88    88 88  `8D 88    88 88'     `8b  d8'
    `8bo.   88    88 88oobY' Y8    8P 88ooooo  `8bd8'
      `Y8b. 88    88 88`8b   `8b  d8' 88~~~~~    88
    db   8D 88b  d88 88 `88.  `8bd8'  88.        88
    `8888Y' ~Y8888P' 88   YD    YP    Y88888P    YP
    """)
    time.sleep(4)
    clear_screen()


welcome()
first_selection()
