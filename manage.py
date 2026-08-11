#!/usr/bin/env python
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sojourn.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django is not installed. Run the project through Docker with "
            "'docker compose up --build'."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
