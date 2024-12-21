"""(C) 2013-2024 Copycat Software, LLC. All Rights Reserved."""

__version__ = "0.5.1"


def enum(**args):
    """Enum."""
    return type("Enum", (), args)
