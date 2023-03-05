""" This module implements the user agent generator, that provides fake user agents for 
    the browsers and operating systems defined in the user_agent_sim_data file.

    Based on the work of: https://github.com/iamdual/ua-generator/
"""

from random         import choice
from typing         import Union
from collections    import defaultdict
from .              import constants as c
from .utils         import SoftwareFactory, AndroidFactory, Software
from ..definitions  import OS_TYPES
from ..template     import BaseGenerator


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
        self.BrowsertoOS = defaultdict(list)
        self.OSs         = [] # available OS names
        self.browsers    = [] # available browser names

        for os, browser in c.TEMPLATES.keys(): 

            self.BrowsertoOS[browser].append(os)

            if os not in self.OSs: 
                self.OSs.append(os)
            
            if browser not in self.browsers: 
                self.browsers.append(browser)

        return


    def _makeOS(self,
        browser: Union[c.NAME_TYPE, c.BRAND_TYPE],   # Name of the selected browser
        device : c.DEVICE_TYPE, # Name of the selected device type
        ) -> Software:
        """ Selects and generates an OS that is compatible with the specified
            browser name and device type.
        """

        # Checks if an OS (given its name) is compatible with a given device type
        isDeviceCompatible = lambda osName, deviceType: OS_TYPES[osName] == deviceType

        # Get browser compatible OS
        browserCompatible  = self.BrowsertoOS[browser]
        
        # Choose one at random if its also device compatible
        osName = choice(
            [name for name in browserCompatible if isDeviceCompatible(name, device)]
        )

        return self.android() if osName == 'android' else self.os(osName) # Make software object
    

    def _makeBrowser(self,
        browserName : Union[c.NAME_TYPE, None], # Browser name. If not provided, pick at random
        ) -> Software:
        """ Selects and generates a browser object """

        # Check input browser name
        if browserName is None:
            print('is none')
            browserName_ = choice(self.browsers)
        else: 
            browserName_ = browserName

        print(browserName, browserName_)
        if not browserName_ in self.browsers:
            raise ValueError(f'Browser {browserName_} is not supported')

        return self.browser(browserName_) # Make Software object


    def _name(self,
        browserName : Union[c.NAME_TYPE, None], # Browser name. If not provided, pick at random
        deviceType  : c.DEVICE_TYPE = 'desktop' # Device type
        ) -> str:
        """ Generates a user agent for the given browser and operating system. """

        browser = self._makeBrowser(browserName)
        os      = self._makeOS(browser.name, deviceType)

        # Select a template (if multiples exist)
        agent = choice(c.TEMPLATES[(os.name, browser.name)])
        
        # Replace version(s) details
        for name in self.OSs     : agent = agent.replace(f'{{{name}}}', os.version)
        for name in self.browsers: agent = agent.replace(f'{{{name}}}', browser.version)
        
        agent = agent.replace('{webkit}', browser.details.get('webkit', '')).\
                      replace('{device}', '; ' + os.details.get('device_name', '')).\
                      replace('{build}' , '; Build/' + os.details.get('build_number', ''))

        return agent