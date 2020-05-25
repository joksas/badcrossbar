from datetime import datetime


def message(message_str, **kwargs):
    """Prints current time followed by a gap and a custom message.

    Parameters
    ----------
    message_str : str
        Message to be printed at the end of the line.
    **kwargs
        verbose : int
            The message is shown only is verbose is equal to 1.
        show_time : bool
            If False, current time is not displayed.

    Returns
    -------
    None
    """
    if kwargs.get('verbose', 1) == 1:
        if kwargs.get('show_time', True):
            time()
            gap(**kwargs)
        print(message_str)


def gap(**kwargs):
    """Prints a given number of whitespace characters.

    Parameters
    ----------
    kwargs
        gap_size : int
            Number of whitespace characters to be printed.
    Returns
    -------
    None
    """
    gap_str = kwargs.get('gap_size', 5)*' '
    print(gap_str, end='')


def time(keep_ms=False):
    """Prints current time.

    Parameters
    ----------
    keep_ms : bool
        If True, includes milliseconds.
    Returns
    -------
    None
    """
    time_str = str(datetime.now())
    if keep_ms is False:
        time_str = time_str.split('.')[0]
    print(time_str, end='')
