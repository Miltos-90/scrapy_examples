""" This module implements the user agent parser, which extracts information from a
    user agent string regarding the browser, operating system, device and engine.
    
    It is based on the ua_parser_py package: https://github.com/vitalibo/ua-parser-py.
"""

import re
from typing        import Tuple, Union, Callable, cast
from .             import constants as c
from ..definitions import Singleton, Browser, CPU, Device, Engine, OS


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

        self.parsers = { # Dictionary of parser callables
            'browser' : lambda x: cast(Browser, self.parse(x, c.BROWSER)),
            'cpu'     : lambda x: cast(CPU, self.parse(x, c.CPU)),
            'device'  : lambda x: cast(Device, self.parse(x, c.DEVICE)),
            'engine'  : lambda x: cast(Engine, self.parse(x, c.ENGINE)),
            'os'      : lambda x: cast(OS, self.parse(x, c.OS))
        }

        self.parseKeys = sorted(self.parsers) # keys sorted order

        return


    def __call__(self, userAgent: str) -> Tuple[Browser, CPU, Device, Engine, OS]:
        """ Parses a user agent string. It returns a dict, whose
            corresponding values are all strings. Keys can be found below.
        """
        
        browser, cpu, device, engine, os = [
            self.parsers[key](userAgent) for key in self.parseKeys
            ]

        browser['majorVersion'] = self._getMajorVersion(browser.get('version', '0.0'))

        return browser, cpu, device, engine, os



    def get(self,
        userAgent : str,              # User agent string
        property  : Tuple[str, str],  # Property whose value will be returned.
        default   : str               # Value to be returned if property is not found
        ) -> str:
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

        return re.sub(r'[^\d\.]', emptyPattern, version).split('.')[0]


    @staticmethod
    def parse(userAgent: str, regexes) -> dict:
        """ Extracts the information needed from a user agent string by the 
            substrings returned by a regex match. 
        """

        matches = False # Regex match from the dictionary
        dict_   = {}
        
        # try matching the user agent with the regexes
        for dict_ in regexes:
            matches = dict_['regex'].search(userAgent)
            if matches: break

        d = {} # Output dictionary

        # Grab all properties in that match
        if matches:
            for i, (key, value) in enumerate(dict_['props'].items()):

                try: match = matches.group(i + 1)
                except IndexError: match = None

                d[key] = Parser._map(match, value)

        return d


    @staticmethod
    def _map(match: Union[re.Match, None], value: Union[str, Callable, None] = None) -> Union[str, re.Match, None]:
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

