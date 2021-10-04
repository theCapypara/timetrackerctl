from typing import List

from timetrackerctl.model.ticket import Ticket
from timetrackerctl.tasks.source import AbstractSource


class SavedSource(AbstractSource):
    @property
    def name(self):
        return "saved"

    def list(self) -> List[Ticket]:
        lst = []
        for t, msg in zip(
                self.jira.list_tickets(self.config.config['tasks'].keys()),
                self.config.config['tasks'].values()
        ):
            t.msg = msg
            t.source = self
            lst.append(t)
        return lst
