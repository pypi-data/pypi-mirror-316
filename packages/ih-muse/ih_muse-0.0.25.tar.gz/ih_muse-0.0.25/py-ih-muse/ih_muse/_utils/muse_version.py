"""Utilities for handling the Muse version."""

try:
    import ih_muse.ih_muse as muse

    _MUSE_VERSION = muse.__version__
except ImportError:
    # This is only useful for documentation
    import warnings

    warnings.warn("Polars binary is missing!", stacklevel=2)
    _MUSE_VERSION = ""


def get_muse_version() -> str:
    """Return the version of the Python IH-Muse package as a string.

    If the Muse binary is missing, returns an empty string.
    """
    return _MUSE_VERSION
