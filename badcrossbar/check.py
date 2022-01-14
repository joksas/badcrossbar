from typing import Any, Optional

import numpy as np
import numpy.typing as npt

from badcrossbar import utils


def crossbar_requirements(
    resistances: npt.ArrayLike,
    applied_voltages: npt.ArrayLike,
    r_i_word_line,
    r_i_bit_line,
    **kwargs,
) -> tuple[npt.NDArray, npt.NDArray]:
    """Checks if crossbar variables satisfy all requirements.

    Args:
        resistances: Resistances of crossbar devices.
        applied_voltages: Applied voltages.
        r_i_word_line: Interconnect resistance of the word line segments.
        r_i_bit_line: Interconnect resistance of the bit line segments.

    Returns:
        Potentially modified resistances and applied voltages.
    """
    resistances, applied_voltages = (np.array(i) for i in (resistances, applied_voltages))
    for value, name in ((resistances, "resistances"), (applied_voltages, "applied_voltages")):
        n_dimensional(value, [2], name)
        numeric_array(value, name)
        non_empty(value, name)

    non_negative_array(resistances, "resistances")
    match_shape(resistances=(resistances, 0), applied_voltages=(applied_voltages, 0))

    for value, name in ((r_i_word_line, "r_i_word_line"), (r_i_bit_line, "r_i_bit_line")):
        if r_i_word_line == r_i_bit_line:
            name = "r_i"
        number(value, name)
        non_negative_number(value, name)

    short_circuit(resistances, r_i_word_line, r_i_bit_line)

    return resistances, applied_voltages


def plotting_requirements(
    device_branch_vals: npt.NDArray = None,
    word_line_branch_vals: npt.NDArray = None,
    bit_line_branch_vals: npt.NDArray = None,
    word_line_node_vals: npt.NDArray = None,
    bit_line_node_vals: npt.NDArray = None,
    branches: bool = True,
) -> npt.NDArray:
    """Checks if arrays containing branch or node values satisfy all
    requirements.

    Args:
        device_branch_vals: Values associated with crossbar devices.
        word_line_branch_vals: Values associated with the interconnect segments
            along the word lines.
        bit_line_branch_vals: Values associated with the interconnect segments
            along the bit lines.
        word_line_node_vals: Values associated with the nodes on the word
            lines.
        bit_line_node_vals: Values associated with the nodes on the bit lines.
        branches: If True, it is assumed that branch values are passed.
            Otherwise, node values are expected.

    Returns:
        Potentially modified branch or nodes values.
    """
    if branches:
        valid_arrays = not_none(
            device_branch_vals=device_branch_vals,
            word_line_branch_vals=word_line_branch_vals,
            bit_line_branch_vals=bit_line_branch_vals,
        )
    else:
        valid_arrays = not_none(
            word_line_node_vals=word_line_node_vals, bit_line_node_vals=bit_line_node_vals
        )
    valid_arrays = {key: np.array(value) for key, value in valid_arrays.items()}

    for key, value in valid_arrays.items():
        numeric_array(valid_arrays[key], key)
        non_empty(valid_arrays[key], key)
        n_dimensional(valid_arrays[key], [2, 3], key)
        valid_arrays[key] = utils.average_if_3D(valid_arrays[key])
        non_infinite_array(valid_arrays[key], key)

    if len(valid_arrays) != 1:
        for dim in [0, 1]:
            dim_arrays = {key: (value, dim) for key, value in valid_arrays.items()}
            match_shape(**dim_arrays)

    if branches:
        return (
            valid_arrays.get("device_branch_vals"),
            valid_arrays.get("word_line_branch_vals"),
            valid_arrays.get("bit_line_branch_vals"),
        )
    else:
        return valid_arrays.get("word_line_node_vals"), valid_arrays.get("bit_line_node_vals")


def not_none(**kwargs: Any) -> dict[str, Any]:
    """Confirms that at least one of the items is not None.

    Args:
        **kwargs: Items of arbitrary type.

    Returns:
        Items that are not None.

    Raises:
        ValueError: If all of the items are None.
    """
    valid_items = {}
    all_none = True
    for key, value in kwargs.items():
        if value is not None:
            all_none = False
            valid_items[key] = value
    if all_none:
        raise ValueError(f"At least one of {', '.join(kwargs)} should be not None!")

    return valid_items


def n_dimensional(array: npt.NDArray, n_list: list[int] = [2], name: str = "array"):
    """Checks that array is `n`-dimensional.

    Args:
        array: Array.
        n_list: Possible number of dimensions.
        name: Name of the variable.

    Raises:
        TypeError: If array is not `n`-dimensional.
    """
    dim = array.ndim
    if dim not in n_list:

        if len(n_list) == 1:
            n_list_str = str(n_list[0])
        else:
            n_list_str = "- or ".join([str(i) for i in n_list])

        raise TypeError(
            f'"{name}" should be {n_list_str}-dimensional array! Instead received {dim}-dimensional array.'
        )


def numeric_array(array: npt.NDArray, name: str = "array"):
    """Checks that array only contains numbers.

    Args:
        array: Array.
        name: Name of the array.

    Raises:
        TypeError: If array contains non-number elements.
    """
    if np.issubdtype(array.dtype, np.number) is False:
        raise TypeError(f'"{name}" should only contain numbers!')


def non_empty(array: npt.NDArray, name: str = "array"):
    """Checks that array is not empty.

    Args:
        array: Array.
        name: Name of the array.

    Raises:
        ValueError: If the array is empty.
    """
    if array.size == 0:
        raise ValueError(f'"{name}" array is empty!')


def match_shape(**kwargs: tuple[npt.NDArray, int]):
    """Checks if arrays have matching dimensions.

    Args:
        **kwargs: Arrays and the dimension along which they should be matched.

    Raises:
        ValueError: If any of the arrays do not match specified dimensions.
    """
    base_key: Optional[str] = None
    base_dim: Optional[int] = None
    base_dim_idx: Optional[int] = None
    for key, value in kwargs.items():
        array = value[0]
        dim_idx = value[1]
        dim = array.shape[dim_idx]
        if base_key is None or base_dim is None:
            base_key = key
            base_dim = dim
            base_dim_idx = dim_idx
            continue
        if dim != base_dim:
            raise ValueError(
                f'Dimension {dim_idx} of array "{key}" should match dimension {base_dim_idx} of array "{base_key}"!'
            )


def non_negative_array(array: npt.NDArray, name: str = "array"):
    """Checks if all the elements of the array are non-negative.

    Args:
        array: Array.
        name: Name of the array.

    Raises:
        ValueError: If the array contains negative values.
    """
    if (array < 0).any():
        raise ValueError(f'"{name}" array contains at least one negative value!')


def non_infinite_array(array: npt.NDArray, name: str = "array"):
    """Checks if all the elements of the array are non-infinite.

    Args:
        array: Array.
        name: Name of the array.

    Raises:
        ValueError: If the array contains positive or negative infinities.
    """
    if (array == np.inf).any() or (array == -np.inf).any():
        raise ValueError(f'"{name}" array contains at least one value with infinite magnitude!')


def number(value: Any, name: str = "variable"):
    """Checks if the variable is a number.

    Args:
        value: Variable of arbitrary type.
        name: Name of the variable.

    Raises:
        TypeError: If the variable is not int or float.
    """
    if not isinstance(value, (int, float)):
        raise TypeError(
            f'Type {type(value).__name__} of "{name}" is not supported. Use int or float instead.'
        )


def non_negative_number(value: float, name: str = "number"):
    """Checks if the number is negative.

    Args:
        value: Number.
        name: Name of the number.

    Raises:
        ValueError: If the number is negative.
    """
    if value < 0:
        raise ValueError(f'"{name}" is negative!')


def short_circuit(resistances: npt.NDArray, r_i_word_line: float, r_i_bit_line: float):
    """Checks if crossbar will be short-circuited.

    This refers to a theoretical scenario when there exists a path of zero
    resistance in a crossbar.

    Args:
        resistances: Resistances of crossbar devices.
        r_i_word_line: Interconnect resistance of the word line segments.
        r_i_bit_line: Interconnect resistance of the bit line segments.

    Raises:
        ValueError: If any of the devices have zero resistance.
    """

    if 0 in resistances:
        if r_i_word_line == r_i_bit_line == 0:
            err_txt = "At least some crossbar devices have zero resistance causing short circuit!"
        else:
            err_txt = (
                "At least some crossbar devices have zero resistance! "
                "This is not currently supported even if it does not "
                "cause short circuit."
            )
        raise ValueError(err_txt)
