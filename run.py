import gspread
import pandas as pd
import os
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
YELLOW = Fore.YELLOW  # yellow text for inputs
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
    if os.name = "posix":
        _ = os.system("clear")
    else:
        _ = os.system("cls")


def first_selection():



def get_age_group():
    """
    Generates an input to ask the user's age and return the age range 
    to which the user belongs
    """

    age = 0
    while age < 1 or age > 100:
        try: 
            age = int(input(YELLOW +'What is yout age?'+ RESET))
            if age < 1 or age > 100:
                print(RED +'Please enter a number between 1 and 100.'+ RESET)
        except ValueError:
            print(RED + 'Please enter a valid number.'+ RESET)
    if  age <= 18:
        return '1-18'
    if  age <= 28:
        return '19-28'
    if  age <= 38:
        return '29-38'
    if  age <= 48:
        return '39-48'
    if  age <= 60:
        return '49-60'
    else:
        return '60+'

# age_group = get_age_group()

# print(WHITE + 'Your age group is:', age_group + RESET)

