from typing import Optional, List, Tuple, Iterable

from timetrackerctl.config import Config
from timetrackerctl.mngmnt.jira_tempo_manager import JiraTempoManager
from timetrackerctl.model.inquiry import Inquiry
from timetrackerctl.model.ticket import Ticket
from timetrackerctl.storage import Storage
from timetrackerctl.tasks.source.recent import RecentSource
from timetrackerctl.tasks.source.saved import SavedSource
from timetrackerctl.tasks.source_provider import get_from_cache


class TicketManager:
    def __init__(self, config: Config, storage: Storage):
        self.config = config
        self.storage = storage
        self.jira = JiraTempoManager(config)

    def current(self) -> Optional[Ticket]:
        return None  # todo

    def open(self) -> bool:
        # TODO: not implemented
        return False

    def open_inquiry(self) -> bool:
        return len(self.current_inquiries()) < 1

    def current_inquiries(self) -> List[Inquiry]:
        """Returns all open inquiries"""
        raise NotImplementedError()

    def recent(self) -> List[Ticket]:
        return RecentSource(self.config, self.storage, self.jira).list()

    def saved(self) -> List[Ticket]:
        return SavedSource(self.config, self.storage, self.jira).list()

    def quick_list(self) -> List[Ticket]:
        return get_from_cache(self.config, self.storage, self.jira)

    def search(self, searched: str) -> List[Ticket]:
        return list(self.jira.search(f'text ~ "{searched}"'))

    def start(self, ticket: str, msg: Optional[str]):
        raise NotImplementedError()

    def track(self, ticket: str, time: str, msg: str):
        raise NotImplementedError()

    def dismiss(self) -> bool:
        raise NotImplementedError()

    def finish(self) -> bool:
        pass
