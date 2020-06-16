from badcrossbar import check
import pytest

not_none_inputs = [{'a': 1, 'b': True, 'c': 'c_str'},
                   {'a': 1, 'b': None, 'c': 'c_str'},
                   {'a': None, 'b': None},
                   {}]
not_none_error = [False, False, True, True]
not_none_results = [{'a': 1, 'b': True, 'c': 'c_str'},
                    {'a': 1, 'c': 'c_str'},
                    {},
                    {}]


@pytest.mark.parametrize('inputs,error,results', [i for i in zip(
    not_none_inputs, not_none_error, not_none_results)])
def test_not_none(inputs, error, results):
    if error:
        with pytest.raises(ValueError):
            check.not_none(**inputs)
    else:
        assert check.not_none(**inputs) == results
