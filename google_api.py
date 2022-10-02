import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime as dt

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

try:
    creds = ServiceAccountCredentials.from_json_keyfile_name("reds.json", scope)
except FileNotFoundError:
    print("File cannot be found.")
else:

    client = gspread.authorize(creds)

    sheet = client.open("MY WORKOUT").sheet1

    sheet_data = sheet.get_all_records()

    date_today = dt.today().strftime('%m/%d/%Y')

    time_now = dt.today().strftime('%H:%M:%S')


def insert_row(time, exercise, duration, calories, date=dt.today().strftime('%m/%d/%Y')):
    new_data = [date, time, exercise, duration, calories]
    sheet.insert_row(new_data, len(sheet_data) + 2)


def insert_col():
    pass
