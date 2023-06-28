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
BLUE = Fore.BLUE  # blue text for tables
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


def first_selection():
    """
    This feature allows users to choose between taking the survey
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
        print("testing survey")
        # get_survey()
    else:
        print("testing results")
        # survey_results()


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
                print(RED + f"Invalid choice. Please enter a number between 1 and {num_options}" + RESET)
        except ValueError:
            print(RED + "Invalid input. Please enter a valid number." + RESET)

    selected_option = options[user_input - 1]
    print(YELLOW + f"You selected: {selected_option}" + RESET)
    user_choices.append(selected_option)

def get_survey():
    """
    This function iterates over a dictionary with columns as keywords
    and num_options as values to generate all the questions for the
    survey.
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

    print("Survey completed")

# first_selection()
get_survey()
print(user_choices)
