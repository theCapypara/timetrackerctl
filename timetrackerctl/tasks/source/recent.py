from datetime import datetime
from typing import List

from timetrackerctl.model.ticket import Ticket
from timetrackerctl.tasks.source import AbstractSource


class RecentSource(AbstractSource):
    @property
    def name(self):
        return "recent"

    def list(self) -> List[Ticket]:
        lst = []
        for h in self.storage.storage['history']:
            lst.append(Ticket(
                self.config, h['ticket'], h['ticket_title'], h['msg'],
                date_for_sort=datetime.utcfromtimestamp(h['start'])
            ))
        return lst
