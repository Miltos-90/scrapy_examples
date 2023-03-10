""" This module implements the user agent parser, which extracts information from a
    user agent string regarding the browser, operating system, device and engine.
    
    Based on the ua_parser_py repo: https://github.com/vitalibo/ua-parser-py.
"""

from .             import regexes as r
from typing        import Tuple, Union, Callable, cast, List, Dict, Literal
from ..definitions import Singleton, Browser, CPU, Device, Engine, OS
import re


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
            'browser' : lambda x: cast(Browser, self.parse(x, r.BROWSER)),
            'cpu'     : lambda x: cast(CPU,     self.parse(x, r.CPU)),
            'device'  : lambda x: cast(Device,  self.parse(x, r.DEVICE)),
            'engine'  : lambda x: cast(Engine,  self.parse(x, r.ENGINE)),
            'os'      : lambda x: cast(OS,      self.parse(x, r.OS))
        }

        self.parseKeys = sorted(self.parsers) # keys in sorted order

        return


    def __call__(self, userAgent: str) -> Tuple[Browser, CPU, Device, Engine, OS]:
        """ Parses a user agent string. It returns a dict, whose
            corresponding values are all strings. Keys can be found below.
        """
        
        browser, cpu, device, engine, os = [self.parsers[key](userAgent) for key in self.parseKeys]
        browser['majorVersion']           = self._getMajorVersion(browser, userAgent)
        
        return browser, cpu, device, engine, os


    def get(self,
        userAgent : str,    # User agent string
        property  : Tuple[  # Property whose value will be returned.
            Literal['browser', 'cpu', 'device', 'engine', 'os'], str],  
        default   : str,    # Value to be returned if property is not found
        ) -> str:
        """ Returns a specific property of the user agent string.
            The full list of properties can be found on templates.py, in the classes
            Browser, CPU, Device, Engine, OS.
        """
        
        name, key = property               # Parser's name and key that the parser should look for
        parser    = self.parsers.get(name) # Get the parser that will provide the key's value

        # Get the key's value
        if parser : return parser(userAgent).get(key, default)
        else      : return default


    @staticmethod
    def _getMajorVersion(browser:Browser, ua:str, default = '1.0', ) -> str:
        """ Extracts major (significant) version from the full browser version. """
        
        version = browser.get('version', default)  # Can return none

        if not version: # If None set to default value
            return default  
        else:           # else, extract it
            return re.sub(r'[^\d\.]', r.EMPTY, version).split('.')[0] 



    @staticmethod
    def parse(userAgent: str, regexes : List[r.REGEXDICT]) -> Dict[str, Union[str, None]]:
        """ Searches the regex list (see regexes.py) for a match with the user
            agent string, and extracts the information needed from a user agent string by the 
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

                try:               match = matches.group(i + 1)
                except IndexError: match = None

                d[key] = Parser._map(match, value)

        return d


    @staticmethod
    def _map(match: Union[str, None], value: Union[str, Callable, None] = None) -> Union[str, None]:
            """ Mapper function. Processes a substring returned as the result of re.group function.
                The returned function modifies <m> (= a regex match object) according to the type of the 
                specified <value>. In particular: 
                    * If value is None, it returns the corresponding match,
                    * if the value is a string, the match is ignored, and the value itself is returned,
                    * if the value is a callable (function) it is being applied to the match, and the
                    result of that operation is returned.
            """

            if value is None:                   return match
            elif isinstance(value, str):        return value
            elif isinstance(value, Callable):   return value(match) if match else None

