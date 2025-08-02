# Module to manipulate paths in os. e.g. extracting file from file path etc
import os.path
# import datetime as dt

# Refresh expired tokens via HTTP requests (?)
from google.auth.transport.requests import Request

# Load saved credentials from token.json
from google.oauth2.credentials import Credentials 

from google_auth_oauthlib.flow import InstalledAppFlow

# Builds Google Calendar API and connects this to Google Calendars
from googleapiclient.discovery import build

from googleapiclient.errors import HttpError

# Define scopes
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def main():
    # Initialize credentials
    creds = None

    # The file token.json stores user's access and refresh tokens and is
    # created automatically when authorization flow completes for the first time

    # If the token exists, user does not have to keep reauthenticating
    if os.path.exists("token.json"):
        # If the token exists, load from the token file and store it in creds
        creds = Credentials.from_authorized_user_file("token.json")

    # Otherwise, user has to log in: if creds does not exist (if don't have credentials)
    # or if credentials are not valid
    if not creds or not creds.valid:
        # Or if creds exist and they're expired and have a refresh token
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # If there's no valid token or refresh token then start a new
            # OAuth flow which is used for first time login or if token is invalid
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            # Later we have to replace with something else. This is just for local testing.
            creds = flow.run_local_server(port=8080)

        # Save the newly obtained credentials to token.json
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        # Build the Google Calendar APi service using the credentials
        service = build("calendar", "v3", credentials=creds)

        # Hard coded for now to test, but later must connect to weather API information
        # Depending on how the information from the weather API is displayed, we can do it another way by directly
        # plugging in variables to dictionary keys (for example, "summary": variable)
        weather = "rain"

        if weather=="rain":
            event = {
                "summary": "Rain",
                "description": "Bring an umbrella.",
                "colorId": 1,
                "start": {
                    "dateTime": "2025-08-03T09:00:00", # Replace hard coding later with information pulled from weather website
                    "timeZone": "America/New_York" # Replace hard coding later with user input
                },
                "end": {
                    "dateTime": "2025-08-03T10:00:00", # Replace hard coding later with information pulled from weather website
                    "timeZone": "America/New_York" # Replace hard coding later with user input
                },
                "recurrence": [
                    "RRULE:FREQ=DAILY;COUNT=3" # Daily for three days; this is just here as a placeholder. Replace later
                ]
            }
        elif weather=="snow":
            event = {
                "summary": "Snow",
                "description": "Wear some boots",
                "colorId": 1,
                "start": {
                    "dateTime": "2025-08-03T09:00:00", # Replace hard coding later with information pulled from weather website
                    "timeZone": "America/New_York" # Replace hard coding later with user input
                },
                "end": {
                    "dateTime": "2025-08-03T10:00:00", # Replace hard coding later with information pulled from weather website
                    "timeZone": "America/New_York" # Replace hard coding later with user input
                },
                "recurrence": [
                    "RRULE:FREQ=DAILY;COUNT=3" # Daily for three days; this is just here as a placeholder. Replace later
                ]
            }
            event = service.events().insert(calendarId="primary", body=event).execute()
        print(f"event created {event.get('htmlLink')}")

    except HttpError as error:
        print("An error occurred: ", error)

if __name__ == "__main__":
    main()