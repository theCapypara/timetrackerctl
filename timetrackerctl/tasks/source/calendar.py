import datetime
import os
import re
from typing import List

from appdirs import user_config_dir
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from timetrackerctl.config import Config
from timetrackerctl.mngmnt.jira_tempo_manager import JiraTempoManager
from timetrackerctl.model.ticket import Ticket
from timetrackerctl.storage import Storage
from timetrackerctl.tasks.source import AbstractSource
TOKEN_FILE_PATH = os.path.join(user_config_dir('timetrackerctl'), 'googletoken.json')
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
TICKET_PATTERN = re.compile(r'^(.*) \[((:?\w)+-(:?\d)+)\]$')


class CalendarSource(AbstractSource):
    def __init__(self, config: Config, storage: Storage, jira: JiraTempoManager):
        super().__init__(config, storage, jira)

        creds = None
        if os.path.exists(TOKEN_FILE_PATH):
            creds = Credentials.from_authorized_user_file(TOKEN_FILE_PATH, SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    os.path.join(user_config_dir('timetrackerctl'), config.config['google_calendar']['api_json']),
                    SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(TOKEN_FILE_PATH, 'w') as token:
                token.write(creds.to_json())

        self.service = build('calendar', 'v3', credentials=creds)

    @property
    def name(self):
        return 'calendar'

    def list(self) -> List[Ticket]:
        now = datetime.datetime.utcnow()
        min = (now - datetime.timedelta(days=1)).isoformat() + 'Z'
        max = (now + datetime.timedelta(days=1)).isoformat() + 'Z'
        events_result = self.service.events().list(calendarId='primary', timeMin=min, timeMax=max,
                                                   maxResults=50, singleEvents=True).execute()
        events = events_result.get('items', [])
        tickets = []
        for event in events:
            match = TICKET_PATTERN.match(event['summary'])
            if match:
                tickets.append((
                    match.group(2), match.group(1), datetime.datetime.fromisoformat(
                        event['start'].get('dateTime', event['start'].get('date'))
                    )
                ))

        lst = []
        for t in self.jira.list_tickets([t[0] for t in tickets]):
            for key, summary, start in tickets:
                if key == t.key:
                    t = t.clone()
                    t.msg = summary
                    t.source = self
                    t.set_sort_date(start)
                    lst.append(t)
        return lst
