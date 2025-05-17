#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_booking.settings_postgres')
    
    # Determine if we're running the development server
    if len(sys.argv) >= 2 and sys.argv[1] == 'runserver':
        print("Running in development mode - applying local settings overrides")
        os.environ['DJANGO_LOCAL_DEVELOPMENT'] = 'True'
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
