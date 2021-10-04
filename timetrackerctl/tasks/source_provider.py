import os
import pickle
from typing import List

from appdirs import user_config_dir

from timetrackerctl.config import Config
from timetrackerctl.mngmnt.jira_tempo_manager import JiraTempoManager
from timetrackerctl.model.ticket import Ticket
from timetrackerctl.storage import Storage
from timetrackerctl.tasks.source.calendar import CalendarSource
from timetrackerctl.tasks.source.github_prs import GithubPrsSource
from timetrackerctl.tasks.source.internal import InternalSource
from timetrackerctl.tasks.source.recent import RecentSource
from timetrackerctl.tasks.source.saved import SavedSource
from timetrackerctl.tasks.source.todoist import TodoistSource
from timetrackerctl.tasks.source.working_on import WorkingOnSource
CACHE = os.path.join(user_config_dir('timetrackerctl'), 'cache.bin')


def get_from_cache(config: Config, storage: Storage, jira: JiraTempoManager) -> List[Ticket]:
    if not os.path.exists(CACHE):
        regenerate_cache(config, storage, jira)
    with open(CACHE, 'rb') as f:
        return pickle.load(f)


def regenerate_cache(config: Config, storage: Storage, jira: JiraTempoManager):
    binary = get_from_sources(config, storage, jira)
    with open(CACHE, 'wb') as f:
        pickle.dump(binary, f)


def get_from_sources(config: Config, storage: Storage, jira: JiraTempoManager) -> List[Ticket]:
    return sorted(
        CalendarSource(config, storage, jira).list() +
        GithubPrsSource(config, storage, jira).list() +
        InternalSource(config, storage, jira).list() +
        RecentSource(config, storage, jira).list() +
        SavedSource(config, storage, jira).list() +
        TodoistSource(config, storage, jira).list() +
        CalendarSource(config, storage, jira).list() +
        WorkingOnSource(config, storage, jira).list(),
        reverse=True
    )
