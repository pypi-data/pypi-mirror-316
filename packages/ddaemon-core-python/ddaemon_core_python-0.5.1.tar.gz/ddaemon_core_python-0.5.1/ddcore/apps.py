"""(C) 2013-2024 Copycat Software, LLC. All Rights Reserved."""

from importlib import import_module

from django.apps import AppConfig


class DDCoreConfig(AppConfig):
    """Docstring."""

    name = "ddcore"

    def ready(self):
        """Docstring."""
        import_module("ddcore.tasks")
