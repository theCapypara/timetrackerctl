import os
from typing import TypedDict, List

import yaml
from appdirs import user_config_dir


class StorageDictHistoryEntry(TypedDict):
    ticket: str
    ticket_title: str
    msg: str
    start: float


class StorageDict(TypedDict):
    start: int
    ticket: str
    ticket_title: str
    msg: str
    history: List[StorageDictHistoryEntry]


class Storage:
    def __init__(self, storage_filename=None):
        if storage_filename is None:
            storage_filename = self.get_default_storage_name()
        self.storage_filename = storage_filename
        self.storage: StorageDict = self._load_storage(storage_filename)
        if "start" not in self.storage:
            self.storage["start"] = -1
        if "ticket" not in self.storage:
            self.storage["ticket"] = ""
        if "ticket_title" not in self.storage:
            self.storage["ticket_title"] = ""
        if "msg" not in self.storage:
            self.storage["msg"] = ""
        if "history" not in self.storage:
            self.storage["history"] = []

    @staticmethod
    def _load_storage(storage_filename) -> dict:
        try:
            with open(storage_filename, 'r') as f:
                return yaml.load(storage_filename)['storage']
        except FileNotFoundError:
            return {}

    @staticmethod
    def get_default_storage_name():
        return os.path.join(user_config_dir('timetrackerctl'), 'storage.yml')
