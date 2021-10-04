from typing import List

from timetrackerctl.tasks.source import AbstractSource


class WorkingOnSource(AbstractSource):
    @property
    def name(self):
        return 'Assigned'

    def list(self):
        lst = []
        statuses = []
        for s in self.config.config['jira']['open_states']:
            statuses.append(f'"{s}"')
        for t in self.jira.search(
                f'assignee="{self.config.config["jira"]["user"]}" AND status IN ({",".join(statuses)}) AND updated >= startOfDay(-30d)',
                modified_for_sort=True
        ):
            t.source = self
            lst.append(t)
        return lst
