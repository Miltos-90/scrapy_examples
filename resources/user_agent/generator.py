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
from typing             import Tuple
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
        self.userAgents  = defaultdict(list) # Dict of user agents in the generator. Keys: <browser, device>, value: user agent

        # Read OS types
        with open('./data/os_types.json', mode = 'r', encoding = 'utf-8') as f:
            self.osTypes = json.load(f)
        
        return


    def _makeAgent(self,
        browserName : BROWSER_TYPE = 'chrome',   # Browser name
        deviceType  : DEVICE_TYPE  = 'desktop'   # Device type
        ) -> Tuple[BROWSER_TYPE, DEVICE_TYPE, str]:
        """ Returns a randomly selected user agent from the given
            device type and browser names. This is the default 
            implementation, which applies to the Scraper and the Reader
        """

        uaString = None # Start with an empty user agent string

        # Get a randomly selected user agent string for the selected browser 
        # and device type (if one exists)
        applicableAgents = self.userAgents.get( (browserName, deviceType) )

        if applicableAgents: # Valid user agent found. Exit
            uaString = choice(applicableAgents)

        else: # No user agent is found (due to invalid browser name/ device type combination).
            
            # Gather all data for the selected device type
            applicableAgentsandBrowsers = []
            for (curName, curDevice), uaString in self.userAgents.items():
                if curDevice == deviceType:
                    applicableAgentsandBrowsers.append((curName, uaString))

            # Select agent from another browser, for the same device type (if one exists)
            if applicableAgentsandBrowsers:
                browserName, uaStrings = choice(applicableAgentsandBrowsers)
                uaString = choice(uaStrings)

            else: # Agents from another browser for this device type are not found, flip device type and try again
                if   deviceType == 'desktop': deviceType = 'mobile'
                elif deviceType == 'mobile' : deviceType = 'desktop'

                # Recurse
                browserName, deviceType, uaString = self._makeAgent(browserName, deviceType)

                # If this is still empty, throw error.
                if not uaString: raise ValueError(f'No valid user agent was found.')

        # Return input arguments as well, in case they were overwritten
        return browserName, deviceType, uaString 


    def __call__(self,  
        deviceType  : DEVICE_TYPE  = 'desktop', # Device type
        browserName : BROWSER_TYPE = 'chrome'   # Browser name
        ) -> UserAgent:
        """ Returns a randomly selected user agent from the given
            device type and browser names.
        """
        
        browserName, deviceType, agent   = self._makeAgent(browserName, deviceType)
        browser, cpu, device, engine, os = self.parser(agent) 
        clientHints                      = self.chGenerator(browser, cpu, device, os)

        return UserAgent(agent, browser, cpu, device, engine, os, clientHints)

