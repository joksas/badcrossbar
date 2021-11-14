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
