""" This module implements the user agent generator, that provides fake user agents for 
    the browsers and operating systems defined in the user_agent_sim_data file.

    Based on the repo: https://github.com/iamdual/ua-generator/
"""

import sys
sys.path.append("../utils")

from random        import choice
from collections   import defaultdict
from .             import constants as c
from .factories    import SoftwareFactory, AndroidFactory, Software
from ..generator   import BaseGenerator
from definitions   import BROWSER_TYPE, DEVICE_TYPE
from typing        import cast, Tuple


class Programmer(BaseGenerator):
    """ Generates programmatically a randomly-selected user 
        agent according to a set type, OS, and browser 
    """

    def __init__(self):
        """ Initialisation method. Generates necessary lists and dictionaries 
            used by the objects.
        """

        super().__init__()

        # Instantiate generators
        self.os          = SoftwareFactory(c.OS)
        self.android     = AndroidFactory(c.ANDROID)
        self.browser     = SoftwareFactory(c.BROWSERS)
        
        # List of valid OS/browser combinations and name lists
        self.browserToOS = defaultdict(list)
        self.browsers    = [] # available browsers/android brands
        self.OSs         = [] # available OS names

        for os, browser in c.TEMPLATES.keys(): 

            self.browserToOS[browser].append(os)
            if os not in self.OSs           : self.OSs.append(os)
            if browser not in self.browsers : self.browsers.append(browser)

        return


    def _makeOS(self,
        browser : BROWSER_TYPE, # Name of the selected browser/OS/vendor
        device  : DEVICE_TYPE,  # Name of the selected device type
        ) -> Software:
        """ Selects and generates an OS that is compatible with the specified
            browser name and device type.
        """
        
        keyCompatible = self.browserToOS[browser] # Get browser-compatible OSs

        osName = choice( # Choose one at random if its also device compatible
            [name for name in keyCompatible if self.isDeviceCompatible(name, device)]
        )

        return self.android() if osName == 'android' else self.os(osName) # Make software object
    

    def isDeviceCompatible(self, osName: c.SOFTWARE_TYPE, deviceType: DEVICE_TYPE):
        """ Checks if an OS (given its name) is compatible with a given device type """

        return self.osDevice[osName] == deviceType


    def __call__(self,
        browserName : BROWSER_TYPE, # Browser name
        deviceType  : DEVICE_TYPE   # Device type
        ) -> Tuple[BROWSER_TYPE, DEVICE_TYPE, str]:
        """ Generates a random user agent for the given browser and operating system. """

        browser = self.browser(browserName)
        os      = self._makeOS(browserName, deviceType)

        # Select a template (if multiples exist)
        osName, bName = cast(c.OS_TYPE, os.name), cast(BROWSER_TYPE, browser.name)
        agent         = choice(c.TEMPLATES[(osName, bName)])
        
        # Replace version(s) details
        for name in self.OSs     : agent = agent.replace(f'{{{name}}}', os.version)
        for name in self.browsers: agent = agent.replace(f'{{{name}}}', browser.version)
        
        agent = agent.replace('{webkit}', browser.details.get('webkit', '')).\
                      replace('{device}', '; ' + os.details.get('device_name', '')).\
                      replace('{build}' , '; Build/' + os.details.get('build_number', ''))

        return browserName, deviceType, agent