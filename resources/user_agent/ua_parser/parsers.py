""" This module implements the user agent parser, which extracts information from a
    user agent string regarding the browser, operating system, device and engine.
    
    It is based on the ua_parser_py package: https://github.com/vitalibo/ua-parser-py.
"""

import re
from typing    import Callable, Union, Tuple, TypedDict
from ua_parser import constants as c


"""Types of the various properties that the parser user agent will generate """

class Browser(TypedDict, total = True):
    name         : str  # Name of the browser
    version      : str  # Full browser version
    majorVersion : str  # Significant (major) browser version


class CPU(TypedDict, total = True):
    architecture: str   # CPU architecture


class Device(TypedDict, total = True):
    vendor: str         # Device brand 
    model : str         # Device model
    type  : str         # Device type (tablet, mobile, etc.)


class Engine(TypedDict, total = True):
    name    : str       # Engine name (Gecko, Webkit, etc.)
    version : str       # Engine version


class OS(TypedDict, total = True):
    name    : str       # Name of the operating system
    version : str       # Operating system version


""" Generic parser and helper object definition """
class RegexParser(object):
    """ Generic user agent string parser. It extracts information about the browser, cpu, 
        device, engine, and operating system using the regexes defined in the regexes.py file.
    """

    def __init__(
        self, 
        regexList : list, # List of regexes (see constants.py)
        flags     : re.RegexFlag = re.IGNORECASE # Flags for compilation
        ):
        """ Initialisation method. Compiles all regexes in the input list """
        
        self.regexes = regexList
        
        for dict_ in self.regexes:
            dict_['regex'] = re.compile(dict_['regex'], flags)

        return


    def __call__(self, userAgent: str) -> tuple:
        """ Extracts the information needed from a user agent string by the 
            substrings returned by a regex match. 
        """

        for dict_ in self.regexes:
            matches = dict_['regex'].search(userAgent) # try matching the user agent with the regexes
            if matches: break

        d = {} # Output dictionary
        if matches:
            for i, (key, value) in enumerate(dict_['props'].items()):

                try: match = matches.group(i + 1)
                except IndexError: match = None

                d[key] = self.map(match, value)

        return d


    @staticmethod
    def map(match: re.Match, value: Union[str, Callable] = None) -> str:
        """ Mapper function. Processes a substring returned as the result of re.group function.
            The returned function modifies <m> (= a regex match object) according to the type of the 
            specified <value>. In particular: 
                * If value is None, it returns the corresponding match,
                * if the value is a string, the match is ignored, and the value itself is returned,
                * if the value is a callable (function) it is being applied to the match, and the
                result of that operation is returned.
        """

        if value is None:                   return match if match else None
        elif isinstance(value, str):        return value
        elif isinstance(value, Callable):   return value(match) if match else None


class Parser():
    """ User agent string parser. It extracts the following information:
        Browser : name, version, major version
        CPU     : architecture
        Device  : vendor, model, type
        Engine  : name, version
        OS      : name, version
    """

    def __init__(self,
        browserRegexes: list = c.BROWSER,
        deviceRegexes : list = c.DEVICE,
        engineRegexes : list = c.ENGINE,
        cpuRegexes    : list = c.CPU,
        osRegexes     : list = c.OS
        ):
        """ Initialisation method. Instantiates required parsers. 
            The format of the input lists can be found on regexes.py
        """

        self.BrowserParser = RegexParser(browserRegexes)
        self.DeviceParser  = RegexParser(deviceRegexes)
        self.EngineParser  = RegexParser(engineRegexes)
        self.CpuParser     = RegexParser(cpuRegexes)
        self.OsParser      = RegexParser(osRegexes)

        return

    def __call__(self, userAgent: str = None) -> Tuple[Browser, CPU, Device, Engine, OS]:
        """ Parses a user agent string. It returns a dict, whose
            corresponding values are all strings. Keys can be found below.
        """

        if not userAgent: return None

        cpu     = self.CpuParser(userAgent)
        device  = self.DeviceParser(userAgent)
        engine  = self.EngineParser(userAgent)
        os      = self.OsParser(userAgent)
        browser = self.BrowserParser(userAgent)

        browser['majorVersion'] = self._getMajorVersion(browser.get('version'))

        return browser, cpu, device, engine, os


    @staticmethod
    def _getMajorVersion(version:str, emptyPattern: str = ''):
        """ Extracts major (significant) version from the full browser version. """

        if version is None:
            return None
        else:
            return re.sub(r'[^\d\.]', emptyPattern, version).split('.')[0]