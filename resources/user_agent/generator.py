""" This module implements an abstract user agent generator class as a template
    for the concrete user agent scraper, programmer, reader classes (see
    scaper.py, ./ua_programmer/, reader.py submodules).
"""

from .definitions       import UserAgent, BROWSER_TYPE, DEVICE_TYPE
from .ua_parser.parser  import Parser
from abc                import ABC
from .client_hints      import ClientHintGenerator as CHGenerator
from random             import choice
from collections        import defaultdict
import json


class BaseGenerator(ABC):
    """ Generic user agent generator. """

    def __init__(self):

        """ Initialisation method. Additional properties (browsers[list] 
            and userAgents[dict]) are declared in the concrete implementations.
        """

        self.parser      = Parser()          # Parse an  agent string (see ./ua_parser)
        self.chGenerator = CHGenerator       # Get client hints from UserAgent (see ./ua_client_hints)
        
        # The following are populated in the subclasses
        self.browsers    = []                # List of browser names in the generator
        self.userAgents  = defaultdict(list) # List of user agents in the generator

        # Read OS types
        with open('./data/os_types.json', mode = 'r', encoding = 'utf-8') as f:
            self.osTypes = json.load(f)
        
        return


    def _name(self,
        browserName : BROWSER_TYPE = 'chrome',   # Browser name
        deviceType  : DEVICE_TYPE  = 'desktop'   # Device type
        ) -> str:
        """ Returns a randomly selected user agent from the given
            device type and browser names. This is the default 
            implementation, which applies to the Scraper and the Reader
        """

        # Choose one at random if not provided
        # Check input browser name
        #if browserName is None: browserName = choice(self.browsers)

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
        deviceType  : DEVICE_TYPE  = 'desktop', # Device type
        browserName : BROWSER_TYPE = 'chrome'   # Browser name
        ) -> UserAgent:
        """ Returns a randomly selected user agent from the given
            device type and browser names.
        """
        
        name                             = self._name(browserName, deviceType)
        browser, cpu, device, engine, os = self.parser(name) 
        clientHints                      = self.chGenerator(browser, cpu, device, os)

        return UserAgent(name, browser, cpu, device, engine, os, clientHints)

