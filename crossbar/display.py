from datetime import datetime


def reduced(original_shape, new_shape):
    if original_shape != new_shape:
        original_shape_str = str(original_shape[0]) + 'x' + str(original_shape[1])
        new_shape_str = str(new_shape[0]) + 'x' + str(new_shape[1])

        time()
        gap()
        print('Size of effective resistances matrix was reduced from ' + original_shape_str + ' to ' + new_shape_str + '.')


def gap(size=5):
    gap_str = 5*' '
    print(gap_str, end='')


def time(keep_ms=False):
    time_str = str(datetime.now())
    if keep_ms is False:
        time_str = time_str.split('.')[0]
    print(time_str, end='')
