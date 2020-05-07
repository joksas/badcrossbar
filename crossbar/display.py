from datetime import datetime


def reduced(original_shape, new_shape):
    """Prints if and how resistances matrix changed after attempted reduction.

    :param original_shape: Shape of original resistances matrix.
    :param new_shape: Shape of new resistances matrix.
    :return: None
    """
    time()
    gap()
    original_shape_str = str(original_shape[0]) + 'x' + str(original_shape[1])
    new_shape_str = str(new_shape[0]) + 'x' + str(new_shape[1])

    if original_shape != new_shape:
        print('Size of effective resistances matrix reduced from ' + original_shape_str + ' to ' + new_shape_str + '.')
    else:
        print('Size of effective resistances matrix kept at ' + original_shape_str + '.')


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
