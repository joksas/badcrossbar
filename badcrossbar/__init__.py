import logging
import sys
import warnings

warnings.simplefilter("always", ImportWarning)

try:
    from .compute import compute
except ModuleNotFoundError:
    warnings.warn("Could not import `badcrossbar.compute()`!", ImportWarning)

try:
    import badcrossbar.plot
except ModuleNotFoundError:
    warnings.warn("Could not import `badcrossbar.plot`!", ImportWarning)

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s (%(levelname)s): %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
