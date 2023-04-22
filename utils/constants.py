""" This module defines a set of constants that are used  throughout the utils module. """

# Default pragma script for the sqlite database class defined in helpers.py
DB_PRAGMA_DEFAULT = """
    PRAGMA foreign_keys=OFF;
    PRAGMA journal_mode=WAL;
    PRAGMA synchronous=FULL;
"""

# Default values for the settings of the IPSwitchMiddleware defined in middlewares.py
PORT     = 9051
PASSWORD = 'miltos'
PROXY    = 'http://127.0.0.1:8118'