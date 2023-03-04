""" This module implements the user agent parser, which extracts information from a
    user agent string regarding the browser, operating system, device and engine.
    
    It is based on the ua_parser_py package: https://github.com/vitalibo/ua-parser-py.
"""

import re
from typing      import Callable, Union, Tuple
from .           import constants as c
from ..templates import Browser, CPU, Device, Engine, OS, Singleton


""" Generic parser and helper object definition """
class RegexParser(object):
    """ Generic user agent string parser. It extracts information about the browser, cpu, 
        device, engine, and operating system using the regexes defined in the regexes.py file.
    """

    def __init__(
        self, 
        regexList : list,               # List of regexes (see constants.py)
        flags     : re.RegexFlag = re.I # Flags for compilation
        ):
        """ Initialisation method. Compiles all regexes in the input list """
        
        self.regexes = regexList
        
        for dict_ in self.regexes:
            dict_['regex'] = re.compile(dict_['regex'], flags)

        return


    def __call__(self, userAgent: str) -> dict:
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

                d[key] = self._map(match, value)

        return d


    @staticmethod
    def _map(match: re.Match, value: Union[str, Callable] = None) -> str:
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


class Parser(metaclass = Singleton):
    """ User agent string parser. It extracts the following information:
        Browser : name, version, major version
        CPU     : architecture
        Device  : vendor, model, type
        Engine  : name, version
        OS      : name, version
    """

    def __init__(self):
        """ Initialisation method. Instantiates required parsers. 
            The format of the input lists can be found on regexes.py
        """

        self.parsers = {
            'browser' : RegexParser(c.BROWSER),
            'device'  : RegexParser(c.DEVICE),
            'engine'  : RegexParser(c.ENGINE),
            'cpu'     : RegexParser(c.CPU),
            'os'      : RegexParser(c.OS)
        }

        return

    def __call__(self, userAgent: str = None) -> Tuple[Browser, CPU, Device, Engine, OS]:
        """ Parses a user agent string. It returns a dict, whose
            corresponding values are all strings. Keys can be found below.
        """

        if not userAgent: return None

        cpu     = self.parsers['cpu'](userAgent)
        device  = self.parsers['device'](userAgent)
        engine  = self.parsers['engine'](userAgent)
        os      = self.parsers['os'](userAgent)
        browser = self.parsers['browser'](userAgent)

        browser['majorVersion'] = self._getMajorVersion(browser.get('version'))

        return browser, cpu, device, engine, os


    def get(self,
        userAgent : str,             # User agent string
        property  : Tuple[str, str], # Property whose value will be returned.
        default   : str = None       # Value to be returned if property is not found
        ):
        """ Returns a specific property of the user agent string.
            The full list of properties can be found on templates.py, in the classes
            Browser, CPU, Device, Engine, OS.
        """
        
        name, key = property 
        parser    = self.parsers.get(name)

        if parser : return parser(userAgent).get(key, default)
        else      : return default


    @staticmethod
    def _getMajorVersion(version:str, emptyPattern: str = '') -> str:
        """ Extracts major (significant) version from the full browser version. """

        if version is None:
            return None
        else:
            return re.sub(r'[^\d\.]', emptyPattern, version).split('.')[0]