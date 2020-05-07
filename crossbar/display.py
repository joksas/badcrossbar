from datetime import datetime


def reduced(original_shape, new_shape):
    if original_shape != new_shape:
        original_shape_str = str(original_shape[0]) + 'x' + str(original_shape[1])
        new_shape_str = str(new_shape[0]) + 'x' + str(new_shape[1])
        print('Size of effective resistances matrix was reduced from ' + original_shape_str + ' to ' + new_shape_str + '.')
