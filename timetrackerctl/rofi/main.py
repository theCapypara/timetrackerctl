import sys
import traceback
from datetime import datetime
from typing import Callable, Tuple, List, Dict, Optional

from rofi import Rofi
from zenipy import zenipy

from timetrackerctl.config import Config
from timetrackerctl.mngmnt.jira_tempo_manager import JiraTempoManager
from timetrackerctl.mngmnt.ticket_manager import TicketManager
from timetrackerctl.model.ticket import Ticket
from timetrackerctl.storage import Storage
from timetrackerctl.util.timeutil import format_timeframe
r = Rofi(rofi_args=['-i', '-columns', '1'])
SEP1 = '------'
SEP2 = '------ '
SEPS = [SEP1, SEP2]
BACK = '< Back'


def start_quick(tm: TicketManager):
    options = {}
    for t in tm.quick_list():
        if t.msg:
            options[f'{t.key} - {t.title}: {t.msg} [#{t.source.name}]'] = t
        else:
            options[f'{t.key} - {t.title} [#{t.source.name}]'] = t
    options[SEP2] = None
    options[BACK] = None
    selected = r.text_entry('Select', options=options.keys())
    _try_quick_start(tm, options, selected)


def start_saved(tm: TicketManager):
    options = {}
    for saved in tm.saved():
        options[f'{saved.msg}: {saved.key} - {saved.title} [#S]'] = saved
    options[SEP1] = None
    for recent in tm.recent():
        options[f'{recent.msg}: {recent.key} - {recent.title} [#R]'] = recent
    options[SEP2] = None
    options[BACK] = None
    selected = r.text_entry('Select', options=options.keys())
    _try_quick_start(tm, options, selected)


def start_search(tm: TicketManager, searched: str = None):
    search_result = []
    options = {}
    if searched is not None:
        search_result = tm.search(searched)
    if len(search_result) == 1:
        return _start_concrete(tm, search_result[0])
    for res in search_result:
        options[f'{res.key} - {res.title}'] = res
    options[SEP2] = None
    options[BACK] = None
    message = 'Ctrl+Enter: Search for current input'
    if searched:
        message = f'> {searched}\n' + message

    selected = r.text_entry('Search', message=message, options=options.keys())
    _try_quick_start(tm, options, selected)


def _try_quick_start(tm: TicketManager, options: Dict[str, Optional[Ticket]], selected: str):
    if selected is None or selected in SEPS:
        return
    if selected == BACK:
        return run()
    if selected in options:
        assert isinstance(options[selected], Ticket)
        return _start_concrete(tm, options[selected])
    return start_search(tm, selected)


def _start_concrete(tm: TicketManager, t: Ticket):
    raise NotImplementedError()


def dismiss(tm: TicketManager):
    raise NotImplementedError()


def finish(tm: TicketManager):
    raise NotImplementedError()


def track(tm: TicketManager):
    raise NotImplementedError()


def open(tm: TicketManager):
    JiraTempoManager(Config()).show_tempo()


ACTION_MAP: List[Tuple[str, Callable[[TicketManager], None]]] = [
    ('Start: Quick', start_quick),
    ('Start: Recent & Saved Tasks', start_saved),
    ('Start: Full Search', start_search),
    ('Dismiss', dismiss),
    ('Finish', finish),
    ('Track Manually', track),
    ('Open Tempo', open)
]


def run():
    tm = TicketManager(Config(), Storage())
    message = None
    if tm.open():
        t = tm.current()
        message = f'Current ({format_timeframe(datetime.now() - t.start)}): {t.key} - {t.title}'
        if t.msg:
            message += f': {t.msg}'
    index, key = r.select('timetrackerctl >', [a[0] for a in ACTION_MAP], message=message)
    if key != 0:
        return
    ACTION_MAP[index][1](tm)


def handle_inquiry(tm: TicketManager):
    raise NotImplementedError()


if __name__ == '__main__':
    try:
        run()
    except:
        zenipy.error(title='Error!', text=''.join(traceback.format_exception(*sys.exc_info())).replace('<', '(').replace('>', ')'))
