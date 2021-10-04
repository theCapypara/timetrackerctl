from enum import Enum, auto


class Inquiry(Enum):
    """Indicates a status of the currently tracked ticket that should or need to
    be resolved before it can be submitted."""
    # SHOULD:
    # Ask if first ticket of the day to correct start time
    FIRST_TICKET_START_TIME = auto()
    # Ask if pause before to fill
    PAUSE_BEFORE = auto()
    # Ask if very long in progress, to cap end time
    VERY_LONG_TICKET = auto()

    # NEED TO:
    # Ask for message if not set
    MESSAGE_NOT_SET = auto()
