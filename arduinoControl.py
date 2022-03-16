# Name: Ishan Vyas
# Course: CPSC 599.88 
# Assignment 2: Physical Output - EventTennis
# UCID: 30068270
# Due Date: March 17th, 2022

from __future__ import print_function

# Import datetime for getting date and os.path for getting os files
import datetime
import os.path

# Import the pySerial library and time
import serial
import time

# Necessary imports for google calendar api call
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# Intialize the number of events to 0
numberOfEvents = 0

# getEvents functions returns the current number of events in the next 24 hours live from your google calendar
def getEvents():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        today = datetime.datetime.utcnow()
        tommorrow = today + datetime.timedelta(days=1)
        today = today.isoformat() + 'Z'
        tommorrow = tommorrow.isoformat() + 'Z'
        
        # API call to google calendar
        events_result = service.events().list(calendarId='0jh8kokuqarlhm9nft81it7uds@group.calendar.google.com', timeMin=today,timeMax=tommorrow,
                                              maxResults=100, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        # Get the length of the events list 
        numberOfEvents = len(events)
        # Return the length
        return numberOfEvents

    # If there is an error return -1 and throw and error
    except HttpError as error:
        print('An error occurred: %s' % error)
        return -1

# Serail port intialisation.
s = serial.Serial(port='/dev/cu.usbmodem14201', baudrate=9600, timeout=.1)

# Write data to serial port and then read data from serial port
def write_read(x):
    s.write(bytes(x))
    time.sleep(0.05)
    data = s.readline()
    return data

# While the python script is running
while True:
    # Get the number of events from google calendar
    numEvents = getEvents()
    print("The current number of events in the next 24 hours is " + str(numEvents))
    # Write and read from serial port
    value = write_read(numEvents)
    print("The current delay time is " + str(value))
    # Sleep for minimizing api calls
    time.sleep(1)

# Close the serial port, when the while loop is broken
s.close()

# Refrences

# Google Calendar api call code from Google Documentation 
# https://developers.google.com/calendar/api/quickstart/python
