from badcrossbar import check
import pytest
import numpy as np

# not_none()
not_none_inputs = [{'a': 1, 'b': True, 'c': 'c_str'},
                   {'a': 1, 'b': None, 'c': 'c_str'},
                   {'a': None, 'b': None},
                   {}]
not_none_error = [False,
                  False,
                  True,
                  True]
not_none_results = [{'a': 1, 'b': True, 'c': 'c_str'},
                    {'a': 1, 'c': 'c_str'},
                    {},
                    {}]
not_none_arguments = zip(
    not_none_inputs, not_none_error, not_none_results)

# n_dimensional()
n_dimensional_array = [np.array(0),
                       np.array([1, 2, 3]),
                       np.array([[1, 2, 3], [4, 5, 6]]),
                       np.array([[['a', 'b']]])]
n_dimensional_n_list = [[0, 1, 2],
                        [2],
                        [2],
                        [3, 5]]
n_dimensional_error = [False,
                       True,
                       False,
                       False]
n_dimensional_arguments = zip(
    n_dimensional_array, n_dimensional_n_list, n_dimensional_error)

# numeric_array()
numeric_array_array = [np.array([['a', 'b'], ['c', 'd']]),
                       np.array(['a', 'b', 0.5],),
                       np.array([None, 1]),
                       np.array([[0.1, 5], [0.2, 10]])]
numeric_array_error = [True,
                       True,
                       True,
                       False]
numeric_array_arguments = zip(numeric_array_array, numeric_array_error)

# non_empty()
non_empty_array = [np.array([]),
                   np.array([[]]),
                   np.array([1, 2]),
                   np.array([[1, 'a'], [2, 'b']])]
non_empty_error = [True,
                   True,
                   False,
                   False]
non_empty_arguments = zip(non_empty_array, non_empty_error)

# match_shape()
match_shape_inputs = [{'a': (np.array([1, 0]), 0),
                       'b': (np.array([[1, 2, 3], [4, 5, 6]]), 0)},
                      {'a': (np.array([1, 0]), 0),
                       'b': (np.array([[1, 2, 3], [4, 5, 6]]), 1)},
                      {'a': (np.array([[]]), 1),
                       'b': (np.array([[[]]]), 2)}]
match_shape_error = [False,
                     True,
                     False]
match_shape_arguments = zip(match_shape_inputs, match_shape_error)

# non_negative_array()
non_negative_array_array = [np.zeros((5, 5)),
                            np.ones((5, 5)),
                            -np.ones((5, 5)),
                            np.array([0, 1, 2]),
                            np.array([0, -1, -2]),
                            np.array([-8, -1, -2])]
non_negative_array_error = [False,
                            False,
                            True,
                            False,
                            True,
                            True]
non_negative_array_arguments = zip(
    non_negative_array_array, non_negative_array_error)

# non_negative_array()
non_infinite_array_array = [np.zeros((5, 5)),
                            np.inf*np.ones((5, 5)),
                            np.array([0, 1, 2]),
                            np.array([0, -np.inf, -2]),
                            np.array([1, np.inf, 2]),
                            np.array([0, 5e100, 1])]
non_infinite_array_error = [False,
                            True,
                            False,
                            True,
                            True,
                            False]
non_infinite_array_arguments = zip(
    non_infinite_array_array, non_infinite_array_error)

# number()
number_value = [1,
                0.5,
                -3,
                0,
                np.inf,
                None,
                'a',
                np.array([1, 2, 3])]
number_error = [False,
                False,
                False,
                False,
                False,
                True,
                True,
                True]
number_arguments = zip(number_value, number_error)

# non_negative_number()
non_negative_number_value = [0,
                             0.0,
                             1,
                             1.0,
                             -1,
                             -1.0,
                             np.inf,
                             -np.inf]
non_negative_number_error = [False,
                             False,
                             False,
                             False,
                             True,
                             True,
                             False,
                             True]
non_negative_number_arguments = zip(
    non_negative_number_value, non_negative_number_error)


@pytest.mark.parametrize('inputs,error,results', not_none_arguments)
def test_not_none(inputs, error, results):
    if error:
        with pytest.raises(ValueError):
            check.not_none(**inputs)
    else:
        assert check.not_none(**inputs) == results


@pytest.mark.parametrize('array,n_list,error', n_dimensional_arguments)
def test_n_dimensional(array, n_list, error):
    if error:
        with pytest.raises(TypeError):
            check.n_dimensional(array, n_list=n_list)
    else:
        check.n_dimensional(array, n_list=n_list)


@pytest.mark.parametrize('array,error', numeric_array_arguments)
def test_numeric_array(array, error):
    if error:
        with pytest.raises(TypeError):
            check.numeric_array(array)
    else:
        check.numeric_array(array)


@pytest.mark.parametrize('array,error', non_empty_arguments)
def test_non_empty(array, error):
    if error:
        with pytest.raises(ValueError):
            check.non_empty(array)
    else:
        check.non_empty(array)


@pytest.mark.parametrize('inputs,error', match_shape_arguments)
def test_match_shape(inputs, error):
    if error:
        with pytest.raises(ValueError):
            check.match_shape(**inputs)
    else:
        check.match_shape(**inputs)


@pytest.mark.parametrize('array,error', non_negative_array_arguments)
def test_non_negative_array(array, error):
    if error:
        with pytest.raises(ValueError):
            check.non_negative_array(array)
    else:
        check.non_negative_array(array)


@pytest.mark.parametrize('array,error', non_infinite_array_arguments)
def test_non_infinite_array(array, error):
    if error:
        with pytest.raises(ValueError):
            check.non_infinite_array(array)
    else:
        check.non_infinite_array(array)


@pytest.mark.parametrize('value,error', number_arguments)
def test_number(value, error):
    if error:
        with pytest.raises(TypeError):
            check.number(value)
    else:
        check.number(value)


@pytest.mark.parametrize('value,error', non_negative_number_arguments)
def test_non_negative_number(value, error):
    if error:
        with pytest.raises(ValueError):
            check.non_negative_number(value)
    else:
        check.non_negative_number(value)
