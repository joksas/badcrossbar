import logging
from collections import namedtuple

import numpy as np
import numpy.typing as npt
from badcrossbar import utils
from badcrossbar.computing import solve

logger = logging.getLogger(__name__)


Interconnect = namedtuple("Interconnect", ["word_line", "bit_line"])
Solution = namedtuple("Solution", ["currents", "voltages"])
Currents = namedtuple("Currents", ["output", "device", "word_line", "bit_line"])
Voltages = namedtuple("Voltages", ["word_line", "bit_line"])


def solution(
    resistances: npt.NDArray,
    r_i_word_line: float,
    r_i_bit_line: float,
    applied_voltages: npt.NDArray,
    **kwargs
) -> Solution:
    """Extracts branch currents and node voltages of a crossbar in a
    convenient form.

    Args:
        resistances: Resistances of crossbar devices.
        r_i_word_line: Interconnect resistance of the word line segments.
        r_i_bit_line: Interconnect resistance of the bit line segments.
        applied_voltages: Applied voltages.
        **node_voltages: If False, None is returned instead of node voltages.

    Returns:
        Branch currents and node voltages of the crossbar.
    """
    r_i = Interconnect(r_i_word_line, r_i_bit_line)

    if r_i.word_line == r_i.bit_line == np.inf:
        return insulating_interconnect_solution(resistances, applied_voltages, **kwargs)

    v = solve.v(resistances, r_i, applied_voltages)

    extracted_voltages = voltages(v, resistances, **kwargs)
    extracted_currents = currents(extracted_voltages, resistances, r_i, applied_voltages, **kwargs)
    if kwargs.get("node_voltages") is not True:
        extracted_voltages = None
    extracted_solution = Solution(extracted_currents, extracted_voltages)
    return extracted_solution


def currents(
    extracted_voltages: Voltages,
    resistances: npt.NDArray,
    r_i: Interconnect,
    applied_voltages: npt.NDArray,
    **kwargs
) -> Currents:
    """Extracts crossbar branch currents in a convenient format.

    Args:
        extracted_voltages: Crossbar node voltages. It has fields `word_line`
            and `bit_line` that contain the potentials at the nodes on the word
            and bit lines.
        resistances: Resistances of crossbar devices.
        r_i: Interconnect resistances along the word and bit line segments.
        applied_voltages: Applied voltages.
        **all_currents: If False, only output currents are returned, while all
            the other ones are set to None.

    Returns:
        Crossbar branch currents. Named tuple has fields `output`, `device`,
        `word_line` and `bit_line` that contain output currents, as well as
        currents flowing through the devices and interconnect segments of the
        word and bit lines.
    """
    device_i = device_currents(extracted_voltages, resistances)
    output_i = output_currents(extracted_voltages, device_i, r_i)
    if kwargs.get("all_currents"):
        word_line_i = word_line_currents(extracted_voltages, device_i, r_i, applied_voltages)
        bit_line_i = bit_line_currents(extracted_voltages, device_i, r_i)
        logger.info("Extracted currents from all branches in the crossbar.")
    else:
        device_i = word_line_i = bit_line_i = None
        logger.info("Extracted output currents.")

    extracted_currents = Currents(output_i, device_i, word_line_i, bit_line_i)
    return extracted_currents


def voltages(v: npt.NDArray, resistances: npt.NDArray, **kwargs) -> Voltages:
    """Extracts crossbar node voltages in a convenient format.

    Args:
        v: Solution to gv = i in a flattened form.
        resistances: Resistances of crossbar devices.

    Returns:
        Crossbar node voltages. It has fields `word_line` and `bit_line` that
        contain the potentials at the nodes on the word and bit lines.
    """
    word_line_v = word_line_voltages(v, resistances)
    bit_line_v = bit_line_voltages(v, resistances)
    extracted_voltages = Voltages(word_line_v, bit_line_v)
    if kwargs.get("node_voltages"):
        logger.info("Extracted node voltages.")
    return extracted_voltages


def word_line_voltages(v: npt.NDArray, resistances: npt.NDArray) -> npt.NDArray:
    """Extracts voltages at the nodes on the word lines.

    Args:
        v: Solution to gv = i in a flattened form.
        resistances: Resistances of crossbar devices.

    Returns:
        Voltages at the nodes on the word lines.
    """
    v_domain = v[
        : resistances.size,
    ]
    return utils.distributed_array(v_domain, resistances)


def bit_line_voltages(v: npt.NDArray, resistances: npt.NDArray) -> npt.NDArray:
    """Extracts voltages at the nodes on the bit lines.

    Args:
        v: Solution to gv = i in a flattened form.
        resistances: Resistances of crossbar devices.

    Returns:
        Voltages at the nodes on the bit lines.
    """
    v_domain = v[
        resistances.size :,
    ]
    return utils.distributed_array(v_domain, resistances)


def output_currents(
    extracted_voltages: Voltages, extracted_device_currents: npt.NDArray, r_i: Interconnect
) -> npt.NDArray:
    """Extracts output currents.

    Args:
        extracted_voltages: Crossbar node voltages. It has fields `word_line`
            and `bit_line` that contain the potentials at the nodes on the word
            and bit lines.
        extracted_device_currents: Currents flowing through crossbar devices.
        r_i: Interconnect resistances along the word and bit line segments.

    Returns:
        Output currents.
    """
    if r_i.bit_line > 0:
        output_i = (
            extracted_voltages.bit_line[
                -1,
            ]
            / r_i.bit_line
        )
    else:
        output_i = np.sum(extracted_device_currents, axis=0)

    output_i = np.transpose(output_i)
    if output_i.ndim == 1:
        output_i = output_i.reshape(1, output_i.shape[0])
    return output_i


def device_currents(extracted_voltages: Voltages, resistances: npt.NDArray):
    """Extracts currents flowing through crossbar devices.

    Args:
        extracted_voltages: Crossbar node voltages. It has fields `word_line`
            and `bit_line` that contain the potentials at the nodes on the word
            and bit lines.
        resistances: Resistances of crossbar devices.

    Returns:
        Currents flowing through crossbar devices.
    """
    if extracted_voltages.word_line.ndim > 2:
        resistances = np.repeat(
            resistances[:, :, np.newaxis], extracted_voltages.word_line.shape[2], axis=2
        )

    v_diff = extracted_voltages.word_line - extracted_voltages.bit_line
    device_i = v_diff / resistances

    return device_i


def word_line_currents(
    extracted_voltages: Voltages,
    extracted_device_currents: npt.NDArray,
    r_i: Interconnect,
    applied_voltages: npt.NDArray,
) -> npt.NDArray:
    """Extracts currents flowing through interconnect segments along the word
    lines.

    Args:
        extracted_voltages: Crossbar node voltages. It has fields `word_line`
            and `bit_line` that contain the potentials at the nodes on the word
            and bit lines.
        extracted_device_currents: Currents flowing through crossbar devices.
        r_i: Interconnect resistances along the word and bit line segments.
        applied_voltages: Applied voltages.

    Returns:
        Currents flowing through interconnect segments along the word lines.
    """
    if r_i.word_line > 0:
        word_line_i = np.zeros(extracted_device_currents.shape)
        if extracted_voltages.word_line.ndim > 2:
            v_diff = (
                applied_voltages
                - extracted_voltages.word_line[
                    :,
                    0,
                ]
            )
            word_line_i[:, 0,] = (
                v_diff / r_i.word_line
            )
        else:
            v_diff = applied_voltages - extracted_voltages.word_line[:, [0]]
            word_line_i[:, [0]] = v_diff / r_i.word_line

        v_diff = (
            extracted_voltages.word_line[
                :,
                :-1,
            ]
            - extracted_voltages.word_line[
                :,
                1:,
            ]
        )
        word_line_i[:, 1:,] = (
            v_diff / r_i.word_line
        )
    else:
        word_line_i = np.repeat(
            extracted_device_currents[
                :,
                -1:,
            ],
            extracted_device_currents.shape[1],
            axis=1,
        )
        for i in range(1, extracted_device_currents.shape[1]):
            word_line_i[:, :-i,] += np.repeat(
                extracted_device_currents[
                    :,
                    -(1 + i) : -i,
                ],
                extracted_device_currents.shape[1] - i,
                axis=1,
            )

    return word_line_i


def bit_line_currents(
    extracted_voltages: Voltages, extracted_device_currents: npt.NDArray, r_i: Interconnect
) -> npt.NDArray:
    """Extracts currents flowing through interconnect segments along the bit
    lines.

    Args:
        extracted_voltages: Crossbar node voltages. It has fields `word_line`
            and `bit_line` that contain the potentials at the nodes on the word
            and bit lines.
        extracted_device_currents: Currents flowing through crossbar devices.
        r_i: Interconnect resistances along the word and bit line segments.

    Returns:
        Currents flowing through interconnect segments along the bit lines.
    """
    if r_i.bit_line > 0:
        bit_line_i = np.zeros(extracted_device_currents.shape)
        v_diff = (
            extracted_voltages.bit_line[
                :-1,
                :,
            ]
            - extracted_voltages.bit_line[
                1:,
                :,
            ]
        )
        bit_line_i[:-1, :,] = (
            v_diff / r_i.bit_line
        )
        if extracted_voltages.bit_line.ndim > 2:
            v_diff = extracted_voltages.bit_line[
                -1,
                :,
            ]
            bit_line_i[-1, :,] = (
                v_diff / r_i.bit_line
            )
        else:
            v_diff = extracted_voltages.bit_line[[-1], :]
            bit_line_i[[-1], :] = v_diff / r_i.bit_line
    else:
        bit_line_i = np.zeros(extracted_device_currents.shape)
        for i in range(extracted_device_currents.shape[0]):
            bit_line_i[i:, :,] += np.repeat(
                extracted_device_currents[
                    i : i + 1,
                    :,
                ],
                extracted_device_currents.shape[0] - i,
                axis=0,
            )

    return bit_line_i


def insulating_interconnect_solution(
    resistances: npt.NDArray, applied_voltages: npt.NDArray, **kwargs
) -> Solution:
    """Extracts solution when all interconnects are perfectly insulating.

    Args:
        resistances: Resistances of crossbar devices.
        applied_voltages: Applied voltages.
        **all_currents: If False, only output currents are returned, while all
            the other ones are set to None.

    Returns:
        Branch currents and node voltages of the crossbar.
    """
    extracted_voltages = Voltages(None, None)
    if kwargs.get("node_voltages"):
        logger.info(
            "Warning: all interconnects are perfectly insulating! Node voltages are undefined!"
        )

    output_i = np.zeros((applied_voltages.shape[1], resistances.shape[1]))
    if kwargs.get("all_currents", True):
        same_i = np.zeros((resistances.shape[0], resistances.shape[1], applied_voltages.shape[1]))
        same_i = utils.squeeze_third_axis(same_i)
        device_i = word_line_i = bit_line_i = same_i
        logger.info("Extracted currents from all branches in the crossbar.")
    else:
        device_i = word_line_i = bit_line_i = None
        logger.info("Extracted output currents.")

    extracted_currents = Currents(output_i, device_i, word_line_i, bit_line_i)
    extracted_solution = Solution(extracted_currents, extracted_voltages)

    return extracted_solution
