#!/usr/bin/env python
import os
import sys
from socket import gethostname

environment = 'production' if gethostname() == 'gwmanage.hanbiro.com' else 'local'

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "billing.settings." + environment)

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
