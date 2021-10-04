from typing import List

from timetrackerctl.tasks.source import AbstractSource


class InternalSource(AbstractSource):
    @property
    def name(self):
        return 'INT'

    def list(self):
        int = self.config.config["jira"]["internal_tickets"]
        lst = []
        for t in self.jira.search(f'project = "{int["project"]}" AND filter = "{int["filter_name"]}" AND status = Open'):
            t.source = self
            lst.append(t)
        return lst
