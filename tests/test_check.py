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
