from datetime import datetime


def reduced(original_shape, new_shape):
    time()
    gap()
    original_shape_str = str(original_shape[0]) + 'x' + str(original_shape[1])
    new_shape_str = str(new_shape[0]) + 'x' + str(new_shape[1])

    if original_shape != new_shape:
        print('Size of effective resistances matrix reduced from ' + original_shape_str + ' to ' + new_shape_str + '.')
    else:
        print('Size of effective resistances matrix kept at ' + original_shape_str + '.')


def message(message_str):
    time()
    gap()
    print(message_str)


def gap(size=5):
    gap_str = size*' '
    print(gap_str, end='')


def time(keep_ms=False):
    time_str = str(datetime.now())
    if keep_ms is False:
        time_str = time_str.split('.')[0]
    print(time_str, end='')
