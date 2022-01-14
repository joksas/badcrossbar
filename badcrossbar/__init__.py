import logging
import sys
import warnings

warnings.simplefilter("always", ImportWarning)

try:
    from .compute import compute
except ModuleNotFoundError as e:
    warnings.warn(f"Could not import `badcrossbar.compute()` ({e})", ImportWarning)

try:
    import badcrossbar.plot
except ModuleNotFoundError as e:
    warnings.warn(f"Could not import `badcrossbar.plot` ({e})", ImportWarning)

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s (%(levelname)s): %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
