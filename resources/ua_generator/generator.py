""" This module implements an abstract user agent generator class as a template
    for the concrete user agent scraper, programmer, reader classes (see
    scaper.py, ./ua_programmer/, reader.py submodules).
"""

import sys
sys.path.append("../definitions") # Adds higher directory to python modules path
sys.path.append("../ua_parser")

from definitions import BROWSER_TYPE, DEVICE_TYPE
from abc         import ABC
from random      import choice
from collections import defaultdict
from typing      import Dict, List, Tuple, get_args
from utils       import readFile
from .parser_adapter import Adapter


class BaseGenerator(ABC):
    """ Generic user agent generator. """

    def __init__(self):

        """ Initialisation method. Additional properties (browsers[list] 
            and userAgents[dict]) are populated in the concrete implementations.
        """

        self.Parser = Adapter() # Adapter (user agent parser)
        
        # Empty user agent dict
        self.userAgents: Dict[Tuple[str, str], List[str]]  = defaultdict(list)

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
        """ Checks if at least one user agent exists in memory. Raises an error if not """

        if not bool(self.userAgents):
            raise ValueError(f'No valid user agents have been added.')
        
        else:
            ratio = self.succesfulImports / (self.unsuccesfulImports + self.succesfulImports) * 100
            ratio = round(ratio, 1)
            print(f'Succesfully imported {self.succesfulImports} user agents ({ratio} % of total).')


    def _getAttribute(self, userAgent: str, attribute: tuple) -> str:
        """ Get an attribute of the user agent string. """

        return self.Parser.get(userAgent, attribute).lower()


    # Setters
    def _add(self, userAgent: str):
        """ Adds a user agent to the dictionary """

        browser = self._getAttribute(userAgent, ('browser', 'name'))
        device  = self._getAttribute(userAgent, ('device', 'type'))

        case1 = browser in get_args(BROWSER_TYPE)
        case2 = device in get_args(DEVICE_TYPE)

        if case1 and case2:

            # If the user agent is an appropriate browser/device combo, add it to the list
            self.succesfulImports += 1
            self.userAgents[browser, device].append(userAgent)
            with open('./in.txt', mode = 'a', encoding='utf-8') as fn:
                fn.write(f'browser: {browser}, device: {device}, \t\t agent: {userAgent}\n')
        
        else:
            # Ignore and show warning
            self.unsuccesfulImports += 1
            #warnings.warn(f'The following user agent has been ignored: {userAgent}')
            with open('./out.txt', mode = 'a', encoding='utf-8') as fn:
                fn.write(f'browser: {browser}, device: {device}, \t\t agent: {userAgent}\n')
                #fn.write(f'"{userAgent}",\n')

        return

