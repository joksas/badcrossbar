from datetime import datetime


def message(message_str):
    """Prints current time followed by a gap and a custom message.

    :param message_str: Message to be printed at the end of the line.
    :return: None.
    """
    time()
    gap()
    print(message_str)


def gap(size=5):
    """Prints a given number of whitespace characters.

    :param size: Number of whitespace characters to be printed.
    :return: None.
    """
    gap_str = size*' '
    print(gap_str, end='')


def time(keep_ms=False):
    """Prints current time.

    :param keep_ms: If True, includes milliseconds.
    :return: None.
    """
    time_str = str(datetime.now())
    if keep_ms is False:
        time_str = time_str.split('.')[0]
    print(time_str, end='')
