import datetime
from typing import TYPE_CHECKING

from dateutil.tz import UTC

from timetrackerctl.tasks.source import AbstractSource

if TYPE_CHECKING:
    from timetrackerctl.config import Config


class Ticket:
    def __init__(
            self, config: 'Config', key: str, title: str, msg: str = None,
            start: datetime.datetime = None, end: datetime.datetime = None,
            *, date_for_sort: datetime.datetime = None, source: AbstractSource = None
    ):
        self._config = config
        self._url = config.config['jira']['url'] + '/browse/' + key
        self._key = key
        self._title = title
        self._msg = msg
        self._start = start
        self._end = end
        self._source = source
        self._date_for_sort = None
        self.set_sort_date(date_for_sort)

    def clone(self):
        c = self.__class__(self._config, self._key, self._title)
        vars(c).update(vars(self))
        return c

    @property
    def key(self):
        return self._key

    @property
    def url(self):
        return self._url

    @property
    def title(self):
        return self._title

    @property
    def msg(self):
        return self._msg

    @msg.setter
    def msg(self, value):
        self._msg = value

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        self._source = value

    def set_sort_date(self, value: datetime.datetime):
        if value is not None and value.tzinfo is None:
            value = value.replace(tzinfo=UTC)
        self._date_for_sort = value

    def __lt__(self, other):
        if not isinstance(other, Ticket):
            return NotImplemented
        if self._date_for_sort is not None and other._date_for_sort is None:
            return False
        if self._date_for_sort is None and other._date_for_sort is not None:
            return True
        if self._date_for_sort is None and other._date_for_sort is None:
            return self._key < other._key
        now = datetime.datetime.now(datetime.timezone.utc)
        return abs(now - self._date_for_sort) >= abs(now - other._date_for_sort)
