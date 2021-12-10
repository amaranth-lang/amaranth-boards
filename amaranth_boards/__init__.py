try:
    try:
        from importlib import metadata as importlib_metadata # py3.8+ stdlib
    except ImportError:
        import importlib_metadata # py3.7- shim
    __version__ = importlib_metadata.version(__package__)
except ImportError:
    # No importlib_metadata. This shouldn't normally happen, but some people prefer not installing
    # packages via pip at all, instead using PYTHONPATH directly or copying the package files into
    # `lib/pythonX.Y/site-packages`. Although not a recommended way, we still try to support it.
    __version__ = "unknown" # :nocov:
