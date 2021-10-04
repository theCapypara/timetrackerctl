import datetime
import re

from github import Github

from timetrackerctl.config import Config
from timetrackerctl.mngmnt.jira_tempo_manager import JiraTempoManager
from timetrackerctl.storage import Storage
from timetrackerctl.tasks.source import AbstractSource
TICKET_PATTERN = re.compile(r'^\[?((:?\w)+-(:?\d)+)\]? (.*)$')


class GithubPrsSource(AbstractSource):
    def __init__(self, config: Config, storage: Storage, jira: JiraTempoManager):
        super().__init__(config, storage, jira)

        github: Github = Github(
            login_or_token=config.config['github']['api']
        )
        self.github_org = github.get_organization(config.config['github']['org'])

    @property
    def name(self):
        return 'github'

    def list(self):
        tickets = []
        for repo in self.github_org.get_repos():
            for pr in repo.get_pulls(sort='updated', direction='desc'):
                if pr.updated_at < datetime.datetime.utcnow() - datetime.timedelta(days=5):
                    break
                involves = set()
                for c in pr.get_comments():
                    involves.add(c.user.login)
                for c in pr.get_reviews():
                    involves.add(c.user.login)
                for c in pr.assignees:
                    involves.add(c.login)
                involves.add(pr.user.login)
                if self.config.config['github']['user'] not in involves:
                    continue

                match = TICKET_PATTERN.match(pr.title)
                if match:
                    tickets.append((
                        match.group(1), "Code Review / Tests", pr.updated_at
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
