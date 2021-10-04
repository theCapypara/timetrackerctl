import datetime
from typing import List, Dict

from todoist import TodoistAPI

from timetrackerctl.config import Config
from timetrackerctl.mngmnt.jira_tempo_manager import JiraTempoManager
from timetrackerctl.storage import Storage
from timetrackerctl.tasks.source import AbstractSource


class TodoistSource(AbstractSource):
    def __init__(self, config: Config, storage: Storage, jira: JiraTempoManager):
        super().__init__(config, storage, jira)

        self.api = TodoistAPI(self.config.config['todoist']['api'])

    @property
    def name(self):
        return 'todo'

    def list(self):
        now = datetime.datetime.now()
        self.api.sync()
        tickets = []
        for item in self.api.projects.get_data(self.config.config['todoist']['project_id'])['items']:
            date = datetime.datetime.fromisoformat(item['date_added'][:-1])
            if 'due' in item and item['due'] is not None:
                date = datetime.datetime.fromisoformat(item['due']['date'])
                if date.date() == now.date():
                    date = now
            self._try_add(tickets, item, date)

        for item in self.api.items.get_completed(self.config.config['todoist']['project_id'],
                                                 since=datetime.datetime.now() - datetime.timedelta(days=1)):
            date = datetime.datetime.fromisoformat(item['date_completed'][:-1])
            self._try_add(tickets, item, date)

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

    def _try_add(self, lst: List, item: Dict, date: datetime.datetime):
        for line in item['description'].splitlines():
            if line.startswith(self.config.config['todoist']['line_prefix']):
                ticket = line.replace(self.config.config['todoist']['line_prefix'], '').strip()
                lst.append((ticket, item['content'], date))
