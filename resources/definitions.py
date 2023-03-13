""" Declaration of classes / datatypes used jointly by all modules """

from typing import Literal

BROWSER_TYPE        = Literal['chrome', 'edge', 'firefox', 'safari', 'opera']   # Available browsers
DEVICE_TYPE         = Literal['desktop', 'mobile']                              # Available device types
PARSER_TYPE         = Literal['browser', 'cpu', 'device', 'engine', 'os']       # Parser types (names) used in parser.py, generator.py
UNKNOWN_NAME        = 'unknown'                                                 # Unknown name token. Used for the initialisation of most properties
MAX_USER_AGENT_SIZE = 256                                                       # Maximum num characters comprising a user agent
UNKNOWN_VERSION     = '0.0'                                                     # Unknown version token. Used for the initialisation of most properties