""" Declaration of classes / datatypes used jointly by all modules """

from dataclasses      import dataclass
from typing           import TypedDict, Literal
from abc              import ABCMeta

BROWSER_TYPE = Literal['chrome', 'edge', 'firefox', 'safari'] # Available browsers
DEVICE_TYPE  = Literal['desktop', 'mobile']                   # Available device types
BASE_URL     = 'http://www.useragentstring.com/pages/useragentstring.php?name={name}' # URL from which to scrape from

class Browser(TypedDict, total = True):     # Browser dictionary
    name         : BROWSER_TYPE             # Name of the browser
    version      : str                      # Full browser version
    majorVersion : str                      # Significant (major) browser version

class CPU(TypedDict, total = True):         # CPU dictionary
    architecture: str                       # CPU architecture

class Device(TypedDict, total = True):      # Device dictionary
    vendor: str                             # Device brand 
    model : str                             # Device model
    type  : DEVICE_TYPE                     # Device type (tablet, mobile, etc.)

class Engine(TypedDict, total = True):      # Engine dictionary
    name    : str                           # Engine name (Gecko, Webkit, etc.)
    version : str                           # Engine version

class OS(TypedDict, total = True):          # Operating system dictionary
    name    : str                           # Name of the operating system
    version : str                           # Operating system version

class ClientHints(TypedDict, total = True): # User agent client hints dictionary
    Sec_CH_UA                   : str       # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-CH-UA
    Sec_CH_UA_Arch              : str       # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-CH-UA-Arch
    Sec_CH_UA_Bitness           : str       # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-CH-UA-Bitness
    Sec_CH_UA_Full_Version_List : str       # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-CH-UA-Full-Version-List
    Sec_CH_UA_Mobile            : str       # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-CH-UA-Mobile
    Sec_CH_UA_Model             : str       # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-CH-UA-Model
    Sec_CH_UA_Platform          : str       # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-CH-UA-Platform
    Sec_CH_UA_Platform_Version  : str       # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-CH-UA-Platform-Version

@dataclass
class UserAgent():                          # User agent struct
    name        : str                       # User agent name
    browser     : Browser                   # Browser dictionary
    cpu         : CPU                       # CPU dictionary
    device      : Device                    # Device dictionary
    engine      : Engine                    # Engine dictionary
    os          : OS                        # Operating system dictionary
    clientHints : ClientHints               # Client hints dictionary


class Singleton(ABCMeta):
    """ Singleton metaclass """
    _instances = {}

    def __call__(cls, *args, **kwargs):

        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]

