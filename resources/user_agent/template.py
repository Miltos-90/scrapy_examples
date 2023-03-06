""" This module implements an abstract user agent generator class as a template
    for the concrete user agent scraper, programmer, reader classes (see
    ua_scaper, ua_programmer, ua_reader submodules).
"""

from .definitions     import UserAgent
from .ua_parser       import Parser
from abc              import ABC
from .ua_client_hints import ClientHintGenerator as CHGenerator
from random           import choice
from collections      import defaultdict
from typing           import Union
import json


class BaseGenerator(ABC):
    """ Generic user agent generator. """

    def __init__(self):

        """ Initialisation method. Additional properties (browsers[list] 
            and userAgents[dict]) are declared in the concrete implementations.
        """

        self.parser      = Parser()          # Parse an  agent string (see ./ua_parser)
        self.chGenerator = CHGenerator       # Get client hints from UserAgent (see ./ua_client_hints)
        
        # Implemented in concrete classes
        self.browsers    = []                # List of browser names in the generator
        self.userAgents  = defaultdict(list) # List of user agents in the generator

        # Read OS types
        with open('./data/os_types.json', mode = 'r', encoding = 'utf-8') as f:
            self.osTypes = json.load(f)
        
        return


    def _name(self,
        browserName : Union[str, None] = None,   # Browser name
        deviceType  : str = 'desktop' # Device type
        ) -> str:
        """ Returns a randomly selected user agent from the given
            device type and browser names. This is the default 
            implementation, which applies to the Scraper and the Reader
        """

        # Choose one at random if not provided
        if browserName is None: browserName = choice(self.browsers)

        # Get a randomly selected user agent string for the selected browser 
        # and device type if one exists
        applicableAgents = self.userAgents.get( (browserName, deviceType) )

        if applicableAgents: 
            uaString = choice(applicableAgents)

        else:
            # Nothing is found (due to invalid name/type combination).
            raise ValueError(f'No user agent exists for browser {browserName}\
                             and device type {deviceType}.')

        return uaString


    def __call__(self,  
        deviceType  : str = 'desktop',          # Device type
        browserName : Union[str, None] = None   # Browser name
        ) -> UserAgent:
        """ Returns a randomly selected user agent from the given
            device type and browser names.
        """
        
        name                             = self._name(browserName, deviceType)
        browser, cpu, device, engine, os = self.parser(name) 
        clientHints                      = self.chGenerator(browser, cpu, device, os)

        return UserAgent(name, browser, cpu, device, engine, os, clientHints)

