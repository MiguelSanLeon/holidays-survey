import gspread
import pandas as pd
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

