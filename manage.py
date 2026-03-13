#!/usr/bin/env python
"""Django command-line utility."""

import os
import sys


def main() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django not found. Make sure it is installed and the virtual environment "
            "is active."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
