from .anonymizer import setup_presidio

# Need to modify this if we add more endpoints that need different recognizers in different setup functions
__all__ = ["setup_presidio"]

