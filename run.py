import gspread
import pandas as pd
import os
import time
import numpy as np
from tabulate import tabulate
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
BRIGHT = Style.BRIGHT  # bright text
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
    while selection != 1 and selection != 2 and selection != 3:
        try:
            print(WHITE + BRIGHT + "Select an option:\n")
            print("1 - Show the results by age group.")
            print("2 - Show the results by gender.")
            print("3 - Back to main menu.\n" + RESET)
            selection = int(input(YELLOW + "Enter your choice: " + RESET))
            if selection != 1 and selection != 2 and selection != 3:
                clear_screen()
                print(RED + "Invalid choice, please enter 1 or 2" + RESET)
        except ValueError:
            clear_screen()
            print(RED + "Invalid input, please enter a valid number" + RESET)
    clear_screen()
    if selection == 1:
        clear_screen()
        question_selection(df, groupby_col='age group')
    elif selection == 2:
        clear_screen()
        question_selection(df, groupby_col='gender')
    elif selection == 3:
        clear_screen()
        first_selection()


def question_selection(df_raw, groupby_col):
    """
    This function allows the user to choose between the different
    questions and apply filters to selection.
    """
    headers = SHEET.worksheet('predefined_answers').row_values(1)
    age_groups = SHEET.worksheet('predefined_answers').col_values(1)
    genders = SHEET.worksheet('predefined_answers').col_values(2)

    if groupby_col == 'age group':
        print(YELLOW + BRIGHT + "Select an age group:\n" + RESET)
        for n, age_group in enumerate(age_groups[1:], start=1):
            print(YELLOW + BRIGHT + f"{n}. {age_group}" + RESET)
        group_input = 0
        while group_input < 1 or group_input > len(age_groups):
            try:
                group_input = int(
                    input(YELLOW + BRIGHT + "\nChoose an option: " + RESET))
                if group_input < 1 or group_input > len(age_groups):
                    print(RED + "Invalid choice. Please enter a number" +
                          f"between 1 and {age_groups}" + RESET)
            except ValueError:
                print(
                    RED + "Invalid input. Please enter a valid number" + RESET)
        clear_screen()
        group_value = age_groups[group_input]
        filtered_df = df_raw.loc[df_raw['age group'] == group_value]

    elif groupby_col == 'gender':
        print(YELLOW + BRIGHT + "Select a gender:\n" + RESET)
        for n, gender in enumerate(genders[1:], start=1):
            print(YELLOW + BRIGHT + f"{n}. {gender}" + RESET)
        group_input = 0
        while group_input < 1 or group_input > len(genders):
            try:
                group_input = int(input(YELLOW + BRIGHT +
                                  "\nChoose an option: " + RESET))
                if group_input < 1 or group_input > len(genders):
                    print(RED + "Invalid choice. Please enter a number" +
                          f"between 1 and {genders}" + RESET)
            except ValueError:
                print(RED + "Invalid input. Please enter a valid number"
                      + RESET)
        clear_screen()
        group_value = genders[group_input]
        filtered_df = df_raw.loc[df_raw['gender'] == group_value]

    print(WHITE + BRIGHT + "Select a question to show the results.\n")
    print("Then press Enter." + RESET)
    num_of_questions = len(df.columns)-2
    for i, header in enumerate(headers[2:], start=1):
        print(YELLOW + BRIGHT + f"{i}. {header}" + RESET)
    user_input = 0
    while user_input < 1 or user_input > num_of_questions:
        try:
            user_input = int(input(YELLOW + BRIGHT +
                                   "\nEnter your choice: " + RESET))
            if user_input < 1 or user_input > num_of_questions:
                print(RED + "Invalid choice. Please enter a number" +
                      f"between 1 and {num_of_questions}" + RESET)
        except ValueError:
            print(RED + "Invalid input. Please enter a valid number." + RESET)
    question_number = user_input
    display_percentage(filtered_df, groupby_col, question_number, group_value)


def display_percentage(df_raw, groupby_col, question_number, group_value):
    """
    Display the results in percentages for a specific question and group.
    """
    df = df_raw.copy()
    question_col = df.columns[question_number + 1]
    filtered_df = df.loc[df[question_col].notna() & df[question_col] != '']

    # if groupby_col == 'age group':
    #    filtered_df = filtered_df.loc[filtered_df['age group'] == group_value]
    # elif groupby_col == 'gender':
    #    filtered_df = filtered_df.loc[filtered_df['gender'] == group_value]

    total_responses = len(filtered_df)
    question_responses = filtered_df[question_col].value_counts()

    print(BLUE + BRIGHT + f"\nResults for question {question_number}:"
          f"{df.columns [question_number + 1]}\n" + RESET)
    print(f"Group: {groupby_col}")
    print(f"Target: {group_value}\n")

    percentages = question_responses / total_responses * 100
    percentages = percentages.round(2)

    frecuency = '(' + question_responses.map(str) + ')'
    df_group = pd.DataFrame(
        {'Answers': frecuency, 'Percentage': percentages})

    df_group['Percentage'] = df_group['Percentage'].apply(
        lambda x: f"{x:.2f}%")

    print(
        BLUE + BRIGHT + tabulate(df_group, headers='keys', tablefmt='psql')
        + RESET)
    print('Press Enter to continue...')
    call_survey_results()


def call_survey_results():
    input()
    clear_screen()
    survey_results()


def first_selection():
    """
    This function allows users to choose between taking the survey
    and viewing the survey results.
    """
    selection = 0
    while selection != 1 and selection != 2 and selection != 3:
        try:
            print(BLUE + BRIGHT + "MAIN MENU" + RESET)
            print(WHITE + BRIGHT + "Select an option:\n")
            print("1 - Take the Survey.")
            print("2 - View Survey results.")
            print("3 - Exit.\n" + RESET)
            selection = int(input(YELLOW + BRIGHT +
                                  "Enter your choice: " + RESET))
            if selection != 1 and selection != 2 and selection != 3:
                clear_screen()
                print(RED + "Invalid choice, please enter 1 or 2" + RESET)
        except ValueError:
            clear_screen()
            print(RED + "Invalid input, please enter a valid number" + RESET)
    clear_screen()
    if selection == 1:
        get_survey()
    elif selection == 2:
        survey_results()
    elif selection == 3:
        goodbye()


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

    print(YELLOW + BRIGHT + question + RESET)
    for i, option in enumerate(options, start=1):
        print(YELLOW + BRIGHT + f"{i}. {option}" + RESET)
        if i >= num_options:
            break
    user_input = -1
    while user_input < 1 or user_input > num_options:
        try:
            user_input = int(input(YELLOW + BRIGHT +
                             "Enter your choice: " + RESET))
            if user_input < 1 or user_input > num_options:
                print(RED + "Invalid choice. Please enter a number" +
                            f"between 1 and {num_options}" + RESET)
        except ValueError:
            print(RED + "Invalid input. Please enter a valid number." + RESET)

    selected_option = options[user_input - 1]
    print(YELLOW + BRIGHT + f"You selected: {selected_option}" + RESET)
    user_choices.append(selected_option)


def get_survey():
    """
    This function iterates over a dictionary with columns as keywords
    and num_options as values to generate all the questions for the
    survey. Then return a list with all the choosen options.
    """

    data = SHEET.worksheet('predefined_answers').get_all_values()
    df_answers = pd.DataFrame(data[1:], columns=data[0])

    column_keys = len(df_answers.columns)
    column_values = [
        [value for value in df_answers[column].tolist()
            if pd.notna(value) and value != ""]
        for column in df_answers.columns
        ]
    options = [len(sublist) for sublist in column_values]

    survey_questions = {}

    for key, value in zip(range(1, column_keys + 1), options):
        survey_questions[key] = value

    for column, num_options in survey_questions.items():
        display_questions_and_options(column, num_options)

        time.sleep(2)
        clear_screen()

    completed_survey_options()


def update_survey_answers(data):
    """
    Update the survey_answers worksheet with the data provided by the user.
    """
    print(WHITE + BRIGHT + "Updating the survey results...\n" + RESET)
    SHEET.worksheet("survey_answers").append_row(data)
    print(WHITE + BRIGHT + "The survey results has been updated\n" + RESET)


def completed_survey_options():
    """
    Displays various options to the user after completing the survey
    and executes the option that the user requests.
    """
    clear_screen()
    print(BLUE + BRIGHT + "THANK YOU FOR COMPLETING THE SURVEY." + RESET)
    print(WHITE + BRIGHT + "Survey results:")
    for i, choice in enumerate(user_choices):
        print(f"Question {i + 1}. You answer: {choice}" + RESET)
    print(BLUE + BRIGHT +
          "\n1- Not happy with your answwers?.Repeat the survey.")
    print("2- Submit your answers and view survey results.")
    print("3- Submit your answers and exit survey." + RESET)

    user_input = 0

    while user_input < 1 or user_input > 3:
        try:
            user_input = int(input(YELLOW + BRIGHT +
                             "Enter your choice: " + RESET))
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
        goodbye()


def welcome():
    """
    Welcome message to start the holiday survey.
    """
    welcome_message = SHEET.worksheet('other_text').col_values(1)
    instrucctions = SHEET.worksheet('other_text').col_values(2)
    clear_screen()
    print("\n")
    print("\n")
    print("\n")
    print(BLUE + BRIGHT + welcome_message[1] + RESET)
    print("\n")
    print(YELLOW + BRIGHT +
          "                            Loading, please wait...")
    time.sleep(5)
    clear_screen()
    print("\n")
    print("\n")
    print("\n")
    print(WHITE + instrucctions[1].upper())
    print(WHITE + instrucctions[2].upper() + RESET)
    print("\n")
    input(YELLOW + BRIGHT +
          "                            press Enter to continue")
    clear_screen()
    print("\n")
    print("\n")
    print("\n")
    print(WHITE + instrucctions[3].upper())
    print(instrucctions[4].upper())
    print(instrucctions[5].upper())
    print(instrucctions[6].upper() + RESET)
    print("\n")
    input(YELLOW + BRIGHT +
          "                            press Enter to continue")
    clear_screen()
    first_selection()


def goodbye():
    """
    This function creates a goodbye message for the user
    and ask if he really wants to exit.
    """
    selection = 0
    while selection != 1 and selection != 2:
        try:
            print(BLUE + BRIGHT + "Are you sure you want to exit?" + RESET)
            print(YELLOW + BRIGHT + " 1- YES.")
            print(" 2- NO." + RESET)
            selection = int(input(YELLOW + BRIGHT +
                            "Enter your choice: " + RESET))
            if selection != 1 and selection != 2:
                clear_screen()
                print(RED + "Invalid choice, please enter 1 or 2" + RESET)
        except ValueError:
            clear_screen()
            print(RED + "Invalid input, please enter a valid number" + RESET)
    clear_screen()
    if selection == 1:
        goodbye_message = SHEET.worksheet('other_text').col_values(3)
        clear_screen()
        print("\n")
        print("\n")
        print("\n")
        print(BLUE + BRIGHT + goodbye_message[1] + RESET)
        time.sleep(3)
        exit()
    else:
        first_selection()


welcome()
