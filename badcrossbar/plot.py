import cairo
from pathvalidate import sanitize_filepath
import badcrossbar.plotting as plotting
import badcrossbar.utils as utils
import badcrossbar.check as check


def branches(device_vals=None, word_line_vals=None,
             bit_line_vals=None, currents=None, **kwargs):
    """Plots a crossbar array and colors its branches according to the values
    passed. The diagram is saved as a PDF file.

    If `currents` is passed, then it is used to plot the currents in the
    branches. Otherwise, at least one of {`device_vals`, `word_line_vals`,
    `bit_line_vals`} has to be passed.

    Parameters
    ----------
    device_vals : array_like, optional
        Values associated with crossbar devices.
    word_line_vals : array_like, optional
        Values associated with the interconnect segments along the word lines.
    bit_line_vals : array_like, optional
        Values associated with the interconnect segments along the bit lines.
    currents : named tuple, optional
        Crossbar branch currents. It should have fields `device`, `word_line`
        and `bit_line` that contain currents flowing through the devices and
        interconnect segments of the word and bit lines (at least one of them
        should be not None).

    **kwargs
        default_color : tuple of float, optional
            Normalized RGB values of the nodes and certain types of branches
            if their values are not provided.
        wire_scaling_factor : float, optional
            Scaling factor for the width of the word and bit lines.
        device_scaling_factor : float, optional
            Scaling factor for the width of the devices. Also scales the nodes.
        node_scaling_factor : float, optional
            Scaling factor for the diameter of the nodes which is combined
            with `device_scaling_factor`. For example, if one wanted to only
            scale the device width by a factor of 2, but keep the node diameter
            the same, arguments `device_scaling_factor = 2` and
            `node_scaling_factor = 1/2` would have to be passed.
        axis_label : str, optional, optional
            Axis label of the color bar.
        low_rgb : tuple of float, optional
            Normalized RGB value associated with the lower limit.
        zero_rgb : tuple of float, optional
            Normalized RGB value associated with the value of zero.
        high_rgb : tuple of float, optional
            Normalized RGB value associated with the upper limit.
        allow_overwrite : bool, optional
            If True, can overwrite existing PDF files with the same name.
        filename : str, optional
            Filename, excluding PDF extension.
        device : {'memristor', 'resistor_usa', 'resistor_europe'}, optional
            Device type to be drawn.
        significant_figures : int, optional
            Number of significant figures to use for the limits of the color
            bar.
        round_crossings : bool, optional
            Because the circuit of a crossbar array is non-planar, the 2D
            diagram of it will have some wire crossings. If `round_crossings`
            is False, these crossings will be drawn as straight lines.
            Otherwise, they will be drawn as semicircles.
        width : float, optional
            Width of the diagram in millimeters.
    """
    kwargs = plotting.utils.set_defaults(kwargs, True)

    if currents is not None:
        device_vals = currents.device
        word_line_vals = currents.word_line
        bit_line_vals = currents.bit_line

    device_vals, word_line_vals, bit_line_vals = \
        check.plotting_requirements(
            device_branch_vals=device_vals,
            word_line_branch_vals=word_line_vals,
            bit_line_branch_vals=bit_line_vals, branches=True)

    crossbar_shape = utils.arrays_shape(
        device_vals, word_line_vals, bit_line_vals)

    surface_dims, diagram_pos, segment_length, color_bar_pos, color_bar_dims = \
        plotting.crossbar.dimensions(crossbar_shape,
                                     width_mm=kwargs.get('width'))

    filename = plotting.utils.get_filepath(kwargs.get('filename'),
            kwargs.get('allow_overwrite'))

    surface = cairo.PDFSurface(filename, *surface_dims)
    context = cairo.Context(surface)

    low, high = plotting.utils.arrays_range(
        device_vals, word_line_vals, bit_line_vals,
        sf=kwargs.get('significant_figures'))

    plotting.crossbar.bit_lines(
        context, bit_line_vals, diagram_pos, low, high,
        segment_length=segment_length, crossbar_shape=crossbar_shape, **kwargs)

    plotting.crossbar.word_lines(
        context, word_line_vals, diagram_pos, low, high,
        segment_length=segment_length, crossbar_shape=crossbar_shape, **kwargs)

    plotting.crossbar.devices(
        context, device_vals, diagram_pos, low, high,
        segment_length=segment_length, crossbar_shape=crossbar_shape, **kwargs)

    for bit_line in [False, True]:
        plotting.crossbar.nodes(
            context, None, diagram_pos, low, high, bit_line=bit_line,
            segment_length=segment_length, crossbar_shape=crossbar_shape,
            **kwargs)

    plotting.color_bar.draw(context, color_bar_pos, color_bar_dims,
                            low, high, **kwargs)


def nodes(word_line_vals=None, bit_line_vals=None, voltages=None, **kwargs):
    """Plots a crossbar array and colors its nodes according to the values
    passed. The diagram is saved as a PDF file.

    If `voltages` is passed, then it is used to plot the voltages on the
    nodes. Otherwise, at least one of {`word_line_vals`, `bit_line_vals`}
    has to be passed.

    Parameters
    ----------
    word_line_vals : array_like, optional
        Values associated with the nodes on the word lines.
    bit_line_vals : array_like, optional
        Values associated with the nodes on the bit lines.
    voltages : named tuple, optional
        Crossbar node voltages. It should have fields `word_line` and
        `bit_line` that contain the potentials at the nodes on the word and
        bit lines (at least one of them should be not None).

    **kwargs
        default_color : tuple of float, optional
            Normalized RGB values of the branches and certain type of nodes
            if its values are not provided.
        wire_scaling_factor : float, optional
            Scaling factor for the width of the word and bit lines.
        device_scaling_factor : float, optional
            Scaling factor for the width of the devices. Also scales the nodes.
        node_scaling_factor : float, optional
            Scaling factor for the diameter of the nodes which is combined
            with `device_scaling_factor`. For example, if one wanted to only
            scale the device width by a factor of 2, but keep the node diameter
            the same, arguments `device_scaling_factor = 2` and
            `node_scaling_factor = 1/2` would have to be passed.
        axis_label : str, optional, optional
            Axis label of the color bar.
        low_rgb : tuple of float, optional
            Normalized RGB value associated with the lower limit.
        zero_rgb : tuple of float, optional
            Normalized RGB value associated with the value of zero.
        high_rgb : tuple of float, optional
            Normalized RGB value associated with the upper limit.
        allow_overwrite : bool, optional
            If True, can overwrite existing PDF files with the same name.
        filename : str, optional
            Filename, excluding PDF extension.
        device : {'memristor', 'resistor_usa', 'resistor_europe'}, optional
            Device type to be drawn.
        significant_figures : int, optional
            Number of significant figures to use for the limits of the color
            bar.
        round_crossings : bool, optional
            Because the circuit of a crossbar array is non-planar, the 2D
            diagram of it will have some wire crossings. If `round_crossings`
            is False, these crossings will be drawn as straight lines.
            Otherwise, they will be drawn as semicircles.
        width : float, optional
            Width of the diagram in millimeters.
    """
    kwargs = plotting.utils.set_defaults(kwargs, False)

    if voltages is not None:
        word_line_vals = voltages.word_line
        bit_line_vals = voltages.bit_line

    word_line_vals, bit_line_vals = check.plotting_requirements(
        word_line_node_vals=word_line_vals,
        bit_line_node_vals=bit_line_vals, branches=False)

    crossbar_shape = utils.arrays_shape(word_line_vals, bit_line_vals)

    surface_dims, diagram_pos, segment_length, color_bar_pos, color_bar_dims = \
        plotting.crossbar.dimensions(crossbar_shape,
                                     width_mm=kwargs.get('width'))

    filename = plotting.utils.get_filepath(kwargs.get('filename'),
            kwargs.get('allow_overwrite'))

    surface = cairo.PDFSurface(filename, *surface_dims)
    context = cairo.Context(surface)

    low, high = plotting.utils.arrays_range(
        word_line_vals, bit_line_vals,
        sf=kwargs.get('significant_figures'))

    plotting.crossbar.bit_lines(
        context, None, diagram_pos, low, high,
        segment_length=segment_length, crossbar_shape=crossbar_shape, **kwargs)

    plotting.crossbar.word_lines(
        context, None, diagram_pos, low, high,
        segment_length=segment_length, crossbar_shape=crossbar_shape, **kwargs)

    plotting.crossbar.devices(
        context, None, diagram_pos, low, high,
        segment_length=segment_length, crossbar_shape=crossbar_shape, **kwargs)

    for node_voltages, bit_line in zip([word_line_vals, bit_line_vals],
                                       [False, True]):
        plotting.crossbar.nodes(
            context, node_voltages, diagram_pos, low, high, bit_line=bit_line,
            segment_length=segment_length, crossbar_shape=crossbar_shape,
            **kwargs)

    plotting.color_bar.draw(context, color_bar_pos, color_bar_dims,
                            low, high, **kwargs)
