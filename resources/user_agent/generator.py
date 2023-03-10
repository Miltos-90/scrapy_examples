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
from typing             import Dict, List, Tuple, get_args, cast
from utils              import readFile


class BaseGenerator(ABC):
    """ Generic user agent generator. """

    def __init__(self):

        """ Initialisation method. Additional properties (browsers[list] 
            and userAgents[dict]) are populated in the concrete implementations.
        """

        self.parser  = Parser()     # Parses an agent string (see ./ua_parser)
        self.osTypes = readFile('./data/os_types.json') # Read OS types
        
        # Empty user agent dict
        self.userAgents: Dict[Tuple[BROWSER_TYPE, DEVICE_TYPE], List[str]]  = defaultdict(list)

        return


    def _makeAgent(self,
        browser      : BROWSER_TYPE = 'chrome',             # Browser name
        device       : DEVICE_TYPE  = 'desktop',            # Device type
        otherDevices : tuple        = get_args(DEVICE_TYPE) # Other device types to choose from
        ) -> Tuple[BROWSER_TYPE, DEVICE_TYPE, str]:
        """ 
            Returns a randomly selected user agent from the given device type and browser names. 
            This is the default implementation, which applies to the Scraper and the Reader.
            If no user agent for the given browser/device combination is found, the following logic
            is implemented:
            - Get another user agent from a different browser (randomly chosen) from the same device type
            - If this fails, get another user agent from a different browser (randomly chosen) from a different device type
            The two above steps are repeated until we run out of possible device choices. If this happens
            a ValueError is raised
        """

        if not any(otherDevices):
            # No more devices are available to choose from. Raise error
            raise ValueError(f'No valid user agent was found.')

        else:
            # Update available (remaining) devices to choose agents from (in case one is not found with
            # the current device)
            otherDevices = tuple([d for d in otherDevices if d != device])

            # Get a randomly selected user agent string for the selected browser and device type (if one exists)
            applicableAgents = self.userAgents.get( (browser, device), [] )

            if applicableAgents: # Valid user agent found. Exit
                return browser, device, choice(applicableAgents)
            
            else: 
                # No user agent is found (due to invalid browser name/ device type combination).
                # Get all user agents for this device type, even from different browsers
                applicableAgents = self._getDeviceCompatible(device)

                if applicableAgents: # Valid user agent found. Exit
                    return browser, device, choice(applicableAgents)
                
                else:
                    # Agents for this device type are not found (for none of the available browsers).
                    # Choose another device type and re-run procedure with the remaining ones
                    device = choice(otherDevices)

                    return self._makeAgent(browser, device, otherDevices)


    def _getDeviceCompatible(self, deviceType: DEVICE_TYPE) -> List[str]:
        """ Get all available user agents for a given device type """

        applicableAgents = []
        for (_, curDevice), uaStringList in self.userAgents.items():
            
            if curDevice == deviceType:
                applicableAgents.extend(uaStringList)

        return applicableAgents


    def __call__(self,  
        deviceType  : DEVICE_TYPE  = 'desktop', # Device type
        browserName : BROWSER_TYPE = 'chrome'   # Browser name
        ) -> Tuple[DEVICE_TYPE, BROWSER_TYPE, UserAgent]:
        """ Returns a randomly selected user agent from the given
            device type and browser names.
        """
        
        # Make user agent
        browserName, deviceType, agent = self._makeAgent(browserName, deviceType)

        # Parse it
        browser, cpu, device, engine, os = self.parser(agent)

        # Generate client hints
        clientHints = CHGenerator(browser, cpu, device, os)

        # Return the inputs in case they were overwritten in the _makeAgent() function
        return deviceType, browserName, UserAgent(agent, browser, cpu, device, engine, os, clientHints)


    def _check(self):
        """ Checks if user agents exist in memory. Raises an error if not """

        if not bool(self.userAgents):
            raise ValueError(f'No valid user agents have been added.')


    # Getters
    def _getOSname(self, agent: str, default: str = 'unknown') -> str:
        """ Extracts operating system. If no OS is returned, set to 'unknown'. """

        return self.parser.get(agent, ('os', 'name'), default).lower()
    

    def _getDevice(self, name: str, default = 'desktop') -> DEVICE_TYPE:
        """ Get device type from OS name (assume desktop if no device type is returned). """

        return self.osTypes.get(name, default)


    def _getBrowserName(self, agent: str, default = 'unknown') -> BROWSER_TYPE:
        """ Extract browser name. If no name is returned, set to 'unknown'. """

        browser = self.parser.get(agent, ('browser', 'name'), default)
        return cast(BROWSER_TYPE, browser.lower())


    # Setters
    def _add(self, userAgent: str):
        """ Adds a user agent to the dictionary """

        browser = self._getBrowserName(userAgent)
        osName  = self._getOSname(userAgent)
        device  = self._getDevice(osName)

        self.userAgents[browser, device].append(userAgent)

        return 
