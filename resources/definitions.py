""" Declaration of classes / datatypes used jointly by all modules """

from typing import Literal

BROWSER_TYPE = Literal['chrome', 'edge', 'firefox', 'safari', 'unknown'] # Available browsers
DEVICE_TYPE  = Literal['desktop', 'mobile', 'unknown']                   # Available device types

