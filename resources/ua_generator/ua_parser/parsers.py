""" This module implements the user agent parser, which extracts information from a
    user agent string regarding the browser, operating system, device and engine.
    
    It is based on the ua_parser_py package: https://github.com/vitalibo/ua-parser-py.
"""

import re
from typing import Callable, Union
from ua_parser import constants


class RegexParser(object):
    """ User agent string parser. It extracts information about the browser, cpu, 
        device, engine, and operating system using the regexes defined in the regexes.py file.
    """

    def __init__(
        self, 
        regexList : list,                           # List of regexes (see regexes.py)
        flags     : re.RegexFlag = re.IGNORECASE    # Flags for compilation
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

        # loop through all regexes
        for dict_ in self.regexes:

            # try matching the user agent with the regexes
            matches = dict_['regex'].search(userAgent) 

            # try matching the user agent with the regexes
            matches = dict_['regex'].search(userAgent) 
            if matches: break
        
        if matches:

            for i, (key, value) in enumerate(dict_['props'].items()):

                try               : match = matches.group(i + 1)
                except IndexError : match = None
                yield key, self.map(match, value)


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
        browserRegexes : list = constants.BROWSER,
        deviceRegexes  : list = constants.DEVICE,
        engineRegexes  : list = constants.ENGINE,
        cpuRegexes     : list = constants.CPU,
        osRegexes      : list = constants.OS
        ):
        """ Initialisation method. Instantiates required parsers. 
            The format of the input lists can be found on regexes.py
        """

        self.BrowserParser   = RegexParser(browserRegexes)
        self.CpuParser       = RegexParser(cpuRegexes)
        self.DeviceParser    = RegexParser(deviceRegexes)
        self.EngineParser    = RegexParser(engineRegexes)
        self.OsParser        = RegexParser(osRegexes)

        return

    def __call__(self, userAgent: str = None) -> dict:
        """ Parses a user agent string. It returns a dict, whose
            corresponding values are all strings. Keys can be found below.
        """

        d = {                                     # Description: 
            ('browser', 'name')          : None,  # Name of the browser
            ('browser', 'version')       : None,  # Full browser version
            ('browser', 'major_version') : None,  # Significant (major) browser version
            ('cpu',     'architecture')  : None,  # CPU architecture
            ('device',  'vendor')        : None,  # Device brand 
            ('device',  'model')         : None,  # Device model
            ('device',  'type')          : None,  # Device type (tablet, mobile, etc.)
            ('engine',  'name')          : None,  # Engine name (Gecko, Webkit, etc.)
            ('engine',  'version')       : None,  # Engine version
            ('os',      'name')          : None,  # Name of the operating system
            ('os',      'version')       : None,  # Operating system version
        }

        if not userAgent: return d                # Skip all if string is empty
        for key, value in self.BrowserParser(userAgent): d['browser', key] = value
        for key, value in self.CpuParser(userAgent)    : d['cpu', key]     = value
        for key, value in self.DeviceParser(userAgent) : d['device', key]  = value
        for key, value in self.EngineParser(userAgent) : d['engine', key]  = value
        for key, value in self.OsParser(userAgent)     : d['os', key]      = value
        
    
        d['browser', 'major_version'] = self._getMajorVersion(d['browser', 'version'])
        return d


    @staticmethod
    def _getMajorVersion(version:str, emptyPattern: str = ''):
        """ Extracts major (significant) version from the full browser version. """

        if version is None:
            return None
        else:
            return re.sub(r'[^\d\.]', emptyPattern, version).split('.')[0]
