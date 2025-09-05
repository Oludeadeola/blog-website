#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bloggy.settings')
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

# Successfully installed amqp-5.2.0 billiard-4.2.0 celery-5.4.0 click-8.1.7 
# click-didyoumean-0.3.1 click-plugins-1.1.1 click-repl-0.3.0 colorama-0.4.6 kombu-5.3.7 prompt-toolkit-3.0.43 
# python-dateutil-2.9.0.post0 six-1.16.0 vine-5.1.0 wcwidth-0.2.13
