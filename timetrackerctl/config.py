import os
from typing import TypedDict, List

import yaml
from appdirs import user_config_dir
from yaml import SafeLoader


class ConfigDictJiraInternalTickets(TypedDict):
    project: str
    filter_name: str


class ConfigDictJira(TypedDict):
    url: str
    user: str
    api: str
    internal_tickets: ConfigDictJiraInternalTickets
    open_states: List[str]


class ConfigDictTodoist(TypedDict):
    project_id: int
    line_prefix: str
    api: str


class ConfigDictGoogleCalendar(TypedDict):
    api_json: str


class ConfigDictGithub(TypedDict):
    api: str
    org: str
    user: str


class ConfigDict(TypedDict):
    jira: ConfigDictJira
    todoist: ConfigDictTodoist
    google_calendar: ConfigDictGoogleCalendar
    github: ConfigDictGithub
    tasks: dict[str, str]


class Config:
    def __init__(self, config_filename=None):
        if config_filename is None:
            config_filename = self.get_default_config_name()
        self.config_filename = config_filename
        self.config: ConfigDict = self._load_config(config_filename)

    @staticmethod
    def _load_config(config_filename) -> dict:
        with open(config_filename, 'r') as f:
            return yaml.load(f, SafeLoader)['config']

    @staticmethod
    def get_default_config_name():
        return os.path.join(user_config_dir('timetrackerctl'), 'config.yml')

    def save(self):
        with open(self.config_filename, 'w') as f:
            yaml.dump(self.config, default_flow_style=False, sort_keys=False)
