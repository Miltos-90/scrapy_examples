""" This module implements an abstract user agent extractor class as a template
    for the concrete user agent scraper and reader classes (see
    scaper.py, reader.py submodules).
"""

from definitions   import BROWSER_TYPE, DEVICE_TYPE
from abc           import ABC, abstractmethod
from random        import choice
from collections   import defaultdict
from typing        import Dict, List, Tuple, get_args
from ..proxies     import ParserExtractorProxy as Parser
import warnings


class Extractor(ABC):
    """ Generic user agent generator. """

    def __init__(self):

        """ Initialisation method. Additional properties (browsers[list] 
            and userAgents[dict]) are populated in the concrete implementations.
        """

        self.Parser = Parser() # Adapter (user agent parser)
        
        # Empty user agent dict
        self.userAgents: Dict[Tuple[str, str], List[str]] = defaultdict(list)

        # Some counters for statistics
        self.unsuccesfulImports, self.succesfulImports  = 0, 0

        return


    def __call__(self,
        browser      : BROWSER_TYPE,                 # Browser name
        device       : DEVICE_TYPE,                  # Device type
        otherDevices : tuple = get_args(DEVICE_TYPE) # Other device types to choose from
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

                    return self.__call__(browser, device, otherDevices) # Recurse


    def _getDeviceCompatible(self, deviceType: DEVICE_TYPE) -> List[str]:
        """ Get all available user agents for a given device type """

        applicableAgents = []
        for (_, curDevice), uaStringList in self.userAgents.items():
            
            if curDevice == deviceType:
                applicableAgents.extend(uaStringList)

        return applicableAgents


    def _check(self):
        """ Checks for succesfully imported user agents. Will raise error or warning. """

        if self.succesfulImports == 0: 
            # Zero user agents imported -> raise error
            raise ValueError(f'No valid user agents have been succesfully imported.')
        
        elif self.unsuccesfulImports != 0: 
            # Not all user agents imported succesfully -> print warning
            ratio  = self.succesfulImports / (self.unsuccesfulImports + self.succesfulImports) * 100
            msg    = f'Succesfully imported {self.succesfulImports} user agents ({round(ratio, 1)} % of total).'

            warnings.warn(msg, RuntimeWarning)
        
        # else -> unsuccesfulImports = 0 and succesfulImports != 0 (i.e. every single user agent is valid and succesfully imported)
        return 


    def _getAttribute(self, userAgent: str, attribute: tuple) -> str:
        """ Get an attribute of the user agent string. """

        return self.Parser.get(userAgent, attribute).lower()


    def _add(self, userAgent: str):
        """ Adds a user agent to the dictionary """

        browser    = self._getAttribute(userAgent, ('browser', 'name'))
        device     = self._getAttribute(userAgent, ('device', 'type'))
        browserOK  = browser in get_args(BROWSER_TYPE)  # Is valid browser
        deviceOK   = device  in get_args(DEVICE_TYPE)   # Is valid device
        validAgent = browserOK and deviceOK             # Appropriate browser/device combo

        if validAgent: # Add agent to dict
            self.succesfulImports += 1
            self.userAgents[browser, device].append(userAgent)
        
        else: # Ignore user agent
            self.unsuccesfulImports += 1 

        return
    

    @abstractmethod
    def _get(**kwargs):
        """ Populates the userAgents dictionary with user agents, and keeps 
            track of succesful and unsuccesful agent imports.
         """
        raise NotImplementedError('Method not implemented.')
