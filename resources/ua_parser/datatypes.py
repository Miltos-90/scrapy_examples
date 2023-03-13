""" Declaration of classes / datatypes used jointly by all modules """

from definitions import UNKNOWN_VERSION, UNKNOWN_NAME
from dataclasses import dataclass
from typing      import Protocol, ClassVar, Dict
import re


""" Definition of dataclasses used in the parser (see parser.py) """
class Dataclass(Protocol):
    """ Asserts if something is a dataclass.
        Checking for this attribute is currently the most reliable way to ascertain that something is a dataclass
        See: https://stackoverflow.com/questions/54668000/type-hint-for-an-instance-of-a-non-specific-dataclass
    """
    __dataclass_fields__: ClassVar[Dict] 


@dataclass
class Browser:
    version     : str = UNKNOWN_VERSION  # Full browser version
    name        : str = UNKNOWN_NAME     # Name of the browser
    majorVersion: str = UNKNOWN_VERSION

    def __post_init__(self):
        """ Extract major version from full version"""
        self.majorVersion = re.sub(r'[^\d\.]', r'', self.version).split('.')[0]


@dataclass
class CPU:
    architecture: str = UNKNOWN_NAME # CPU architecture


@dataclass
class Device:
    vendor: str = UNKNOWN_NAME      # Device brand 
    model : str = UNKNOWN_NAME      # Device model
    type  : str = UNKNOWN_NAME      # Device type (tablet, mobile, etc.)


@dataclass
class Engine:
    name   : str = UNKNOWN_NAME     # Engine name (Gecko, Webkit, etc.)
    version: str = UNKNOWN_VERSION  # Engine version


@dataclass
class OS:
    name   : str = UNKNOWN_NAME     # Name of the operating system
    version: str = UNKNOWN_VERSION  # Operating system version






