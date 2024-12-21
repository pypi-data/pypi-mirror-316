"""Visualization and post-processing of RF data (e.g., Touchstone files).
Get a presentation and report data fast."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("rf-visuals")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError
