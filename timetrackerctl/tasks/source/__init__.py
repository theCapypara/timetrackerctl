from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from timetrackerctl.config import Config
    from timetrackerctl.mngmnt.jira_tempo_manager import JiraTempoManager
    from timetrackerctl.model.ticket import Ticket
    from timetrackerctl.storage import Storage


class AbstractSource(ABC):
    def __init__(self, config: 'Config', storage: 'Storage', jira: 'JiraTempoManager'):
        self.config = config
        self.storage = storage
        self.jira = jira

    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def list(self) -> List['Ticket']:
        pass
