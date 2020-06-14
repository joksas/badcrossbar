import badcrossbar.utils as utils


def time(**kwargs):
    """Prints current time.

    Parameters
    ----------
    **kwargs
        keep_ms : bool
            If True, includes milliseconds.
    Returns
    -------
    None
    """
    time_str = utils.time(keep_ms=kwargs.get('keep_ms', False))
    print(time_str, end='')
