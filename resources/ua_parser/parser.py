""" This module implements the user agent parser, which extracts information from a
    user agent string regarding the browser, operating system, device and engine.
    
    Based on the ua_parser_py repo: https://github.com/vitalibo/ua-parser-py.
"""

import sys
sys.path.append("../utils")
sys.path.append("../definitions")

from .               import regexes as r
from .               import definitions as defs
from .generic_parser import GenericParser
from typing          import Tuple, get_args
from utils           import Singleton
from definitions     import PARSER_TYPE


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

        self.parsers = { # Dictionary of base parsers
            'browser' : GenericParser(r.BROWSER, defs.Browser),
            'cpu'     : GenericParser(r.CPU,     defs.CPU),
            'device'  : GenericParser(r.DEVICE,  defs.Device),
            'engine'  : GenericParser(r.ENGINE,  defs.Engine),
            'os'      : GenericParser(r.OS,      defs.OS),
        }

        return


    def __call__(self, userAgent: str) -> \
        Tuple[defs.Dataclass, defs.Dataclass, defs.Dataclass, defs.Dataclass,defs.Dataclass]:
        """ Parses a user agent string, returning the following classes (in order of appearance):
            browser, cpu, device, engine, os
        """
        return tuple(self.parsers[key](userAgent) for key in get_args(PARSER_TYPE))

    
    def get(self,
        userAgent : str,                     # User agent string
        attribute : Tuple[PARSER_TYPE, str], # Property whose value will be returned.
        ) -> str:
        """ Returns a specific property of the user agent string.
            The full list of properties can be found on templates.py, in the classes
            Browser, CPU, Device, Engine, OS.
        """

        parserName, propertyName = attribute      # Parser's name and key that the parser should look for        
        parser = self.parsers.get(parserName)    # Get the parser that will provide the key's value

        if parser:
            dClass = parser(userAgent)           # Get object from the corresponding generic parser
            return getattr(dClass, propertyName) # Extract the corresponding key (=property). Raises AttributeError if not found

        else: 
            raise KeyError(f'Parser {parserName} does not exist')


"""

with open('./out copy.txt') as f:
    agents = f.read().splitlines()

agents = [
 "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:40.0) Gecko/20100101 Firefox/40.0.2 Waterfox/40.0.2",
]
P = Parser()
for i, agent in enumerate(agents):
    try:
        pua = P(agent)
        #print(i, pua)
        #print(agent)
        print(i, '\tbrowser\t', pua[0].name, '\tOS\t', pua[-1].name, '\t', agent)
    except:
        print(f'died on {i}')
        print()

"""
