#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Start script for the Recibos TurboGears project.

This script is only needed during development for running from the project
directory. When the project is installed, easy_install will create a
proper start script.
"""
import locale
locale.setlocale(locale.LC_ALL, "")
import sys
from recibos.commands import start, ConfigurationError

if __name__ == "__main__":
    try:
        start()
    except ConfigurationError, exc:
        sys.stderr.write(str(exc))
        sys.exit(1)
