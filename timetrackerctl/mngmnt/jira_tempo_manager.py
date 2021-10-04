import datetime
import webbrowser
from typing import List, Iterable, TYPE_CHECKING

from jira import JIRA, Issue

if TYPE_CHECKING:
    from timetrackerctl.model.ticket import Ticket
    from timetrackerctl.config import Config


class JiraTempoManager:
    def __init__(self, config: 'Config'):
        self.config = config
        self.api = JIRA(
            basic_auth=(config.config['jira']['user'], config.config['jira']['api']),
            options={"server": config.config['jira']['url']}
        )

    def history(self, since: datetime.datetime) -> List['Ticket']:
        raise NotImplementedError()

    def show_tempo(self):
        webbrowser.open_new_tab(self.config.config['jira']['url'] + '/plugins/servlet/ac/io.tempo.jira/tempo-app')

    def list_tickets(self, ticket_keys: Iterable[str]) -> Iterable['Ticket']:
        return self.search(f'key in ({",".join(ticket_keys)})')

    def search(self, jql: str, modified_for_sort=False) -> Iterable['Ticket']:
        from timetrackerctl.model.ticket import Ticket
        for issue in self.api.search_issues(jql):
            issue: Issue
            t = Ticket(
                self.config, issue.key, issue.fields.summary
            )
            if modified_for_sort:
                # thanks jira.
                updated = issue.fields.updated[:-2] + ':' + issue.fields.updated[-2:]
                t.set_sort_date(datetime.datetime.fromisoformat(updated))
            yield t
