from datetime import date, time, timedelta, datetime
from typing import Optional, List

import click
from click import echo
from prettytable import PrettyTable

from timetrackerctl.config import Config
from timetrackerctl.error import AbortError
from timetrackerctl.mngmnt.jira_tempo_manager import JiraTempoManager
from timetrackerctl.mngmnt.ticket_manager import TicketManager
from timetrackerctl.model.ticket import Ticket
from timetrackerctl.rofi.main import run, handle_inquiry
from timetrackerctl.storage import Storage
from timetrackerctl.tasks.source_provider import regenerate_cache
from timetrackerctl.util.timeutil import format_time, format_date, format_timeframe


def current():
    t: Optional[Ticket] = TicketManager(Config(), Storage()).current()
    if not t:
        echo("No ticket is being worked on.")
    else:
        echo(f"Ticket:     {t.key}")
        echo(f"URL:        {t.url}")
        echo(f"Title:      {t.title}")
        echo(f"Task:       {t.msg}")
        echo(f"Started:    {format_time(t.start)} ({format_timeframe(datetime.now() - t.start)} ago)")


@click.group(invoke_without_command=False)
def cli():
    pass


@cli.command()
def ui():
    run()


def _log_print_table(day: datetime, table: PrettyTable):
    print(format_date(day))
    print("===========")
    print(table)


@cli.command()
def log():
    tempo = JiraTempoManager(Config())
    history: List[Ticket] = tempo.history((datetime.combine(date.today(), time(0, 0, 0)) - timedelta(days=1)))
    day = None
    for ticket in history:
        tday = datetime.combine(ticket.start, time(0, 0, 0))
        if tday != day:
            if day is not None:
                _log_print_table(day, t)
            t = PrettyTable()
            t.field_names = ["Ticket", "Start", "Time", "Task"]
            day = tday
        t.add_row([ticket.key, format_time(ticket.start), format_timeframe(ticket.end - ticket.start), ticket.msg])
    _log_print_table(day, t)


@cli.command()
@click.argument('ticket')
@click.argument('msg', required=False)
def start(ticket, msg):
    tm = TicketManager(Config(), Storage())
    if tm.open():
        echo("Currently open ticket will be ended now:")
        current()
        echo("---")
    if tm.open_inquiry():
        echo("Input required.")
        try:
            handle_inquiry(tm)
        except AbortError:
            echo("Abort.")
            return
        echo("Ticket ended.")
        echo("---")
    tm.start(ticket, msg)
    echo("Started new ticket.")
    current()


@cli.command()
@click.argument('ticket')
@click.argument('time')
@click.argument('msg')
def track(ticket, time, msg):
    tm = TicketManager(Config(), Storage())
    tm.track(ticket, time, msg)
    echo("Submitted.")


@cli.command()
def dismiss():
    tm = TicketManager(Config(), Storage())
    if tm.open():
        echo("Dismissing currently open:")
        current()
        echo("---")
        tm.dismiss()
        echo("Dismissed.")
    else:
        echo("Nothing to dismiss.")


@cli.command()
def finish():
    tm = TicketManager(Config(), Storage())
    if tm.open():
        echo("Finishing currently open:")
        current()
        echo("---")
        if tm.open_inquiry():
            echo("Input required.")
            try:
                handle_inquiry(tm)
            except AbortError:
                echo("Abort.")
                return
        tm.finish()
        echo("Finished.")
    else:
        echo("Nothing to finish.")


@cli.command()
def gencache():
    echo("Generating cache...")
    regenerate_cache(Config(), Storage(), JiraTempoManager(Config()))
    echo("Done.")


@cli.command(name='open')
def open_cmd():
    JiraTempoManager(Config()).show_tempo()


if __name__ == '__main__':
    cli()
