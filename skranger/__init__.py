from skranger._version import __version__

# Import the compiled ranger module
try:
    from skranger import ranger
except ImportError:
    # This handles the case where the .so file is missing
    import warnings
    warnings.warn("Failed to import the compiled ranger module. The package may not work correctly.")
