""" This module implements the user agent generator, that provides fake user agents for 
    the browsers and operating systems defined in the user_agent_sim_data file.

    Based on the work of: https://github.com/iamdual/ua-generator/
"""

from random            import randint, choice
from collections       import defaultdict
from .                 import constants as c
from ..templates       import Software, UserAgent
from ..ua_client_hints import ClientHintGenerator as CH
from ..ua_parser       import Parser
import string


class SoftwareFactory():
    """ Generic software generator. It provides random software versions and their corresponding details
    """

    def __init__(self, versions: dict):
        
        self.versions = versions
        self.names    = list(versions.keys())
        return


    def __call__(self, name: str) -> Software:
        """ Randomly chooses a software version and its associated details from its name"""
        
        versions = self.versions[name] # Get versions relevant to software <name>

        # if only keys are specified in the data (i.e. the structure is a set), convert to dict
        if isinstance(versions, set): versions = dict.fromkeys(versions, {})

        # Select version from those
        majorVersion   = choice(list(versions.keys())) # Randomly select major version number
        versionDetails = versions[majorVersion]        # Additional details associated with this version
        
        # Randomly select minor version number
        minorRange     = versionDetails.get('minor_range')
        minorVersion   = randint(minorRange[0], minorRange[1]) if minorRange else None

        return Software(
            name    = name,
            details = self._makeDetails(majorVersion, str(minorVersion), versionDetails),
            version = self._makeVersionString(majorVersion, minorVersion = minorVersion, name = name),
        )


    @staticmethod
    def _makeDetails(
        majorVersion      : str, # Major version of the software 
        minorVersion      : str, # Ninor version of the software 
        versionProperties : dict # Additional software details 
        ) -> dict:
        """ Generates all addditional details of a major version of a software """

        # Loop over all properties and populate dictionary
        d = {'major_version' : majorVersion,
             'minor_version' : minorVersion}
            
        for propKey, propValue in versionProperties.items():
            if propKey != 'minor_range':  d[propKey] = propValue                

        return d


    @staticmethod
    def _makeVersionString(
        majorVersion: str,      # Major (significant) versin of the software
        **kwargs
        ) -> str:
        """ Makes version string for a software given its main properties. """
    
        minorVer = kwargs.get("minorVersion")
        name     = kwargs.get("name")
        version  = majorVersion # Start with the major version

        if not SoftwareFactory._skipMinorVersion(name, minorVer): 
            version += '.' + str(minorVer)

        if name in ['macos', 'ios']: 
            version = version.replace('.', '_')
        
        return version


    @staticmethod
    def _skipMinorVersion(
        name         : str,     # Software name
        minorVersion : int      # Minor version of the software
        ) -> bool:
        """ Evaluates whether or not the minor software version
            should be included in the version string
        """

        # Some software truncates the trailing '.0' pattern during versions
        l = ['macos', 'ios', 'firefox']
        if name in l : stripZero = True
        else         : stripZero = False

        # Do not include minor version in the following cases
        return (minorVersion is None) or (minorVersion == 0 and stripZero)


class AndroidFactory(SoftwareFactory):
    """ Generic Android OS generator. """

    def __init__(self, 
        systems: dict # Dictionary containing the details of the system
        ):
        
        super().__init__(systems['versions'])
        self.devices = systems['devices']

        return
    

    def __call__(self, 
        brand: str = None # Android device brand (e.g. samsung, nexus, etc.) 
        ) -> dict:
        """ Generate a random Android OS """

        # Randomly select a brand of mobile phones operating on Android and make OS
        if brand is None: brand = choice(self.names)
        
        # Make os
        os = super(AndroidFactory, self).__call__(brand)
        os.name                     = 'android' # overwrite with OS name
        os.details['brand']         = brand
        os.details['device_name']   = choice(self.devices[brand])
        os.details['build_number']  = self._buildNumber(os.details['build_number'])
        
        return os


    @staticmethod
    def _buildNumber(
        buildNumbers : tuple    # Avaliable build numbers to choose from
        ) -> str:
        """ Formats the buildnumber according to the mmanufacturer. 
            Supports nexus, samsung and pixel devices.
        """

        buildNum   = choice(buildNumbers)   # Choose a build number at random.
        formatters = (                      # Generate random formatters for the build number.
            {'from': '{s}', 'to' : '{}'.format(choice(string.ascii_uppercase))},
            {'from': '{d}', 'to' : '{:02d}{:02d}{:02d}'.format(randint(17, 22), randint(0, 12), randint(0, 29))},
            {'from': '{v}', 'to' : '{}'.format(randint(1, 255))}
        )

        for f in formatters: buildNum = buildNum.replace(f['from'], f['to'])

        return buildNum


    @staticmethod
    def _makeVersionString(majorVersion: str, **kwargs) -> str: return majorVersion.replace('.0', '')       


class Maker():
    """ Generates a randomly-selected user agent according to a set type, OS, and browser """

    def __init__(self):

        # Instantiate generators
        self.os      = SoftwareFactory(c.OS)
        self.android = AndroidFactory(c.ANDROID)
        self.browser = SoftwareFactory(c.BROWSERS)

        # List of valid OS/browser combinations and name lists
        self.BrowsertoOS = defaultdict(list)
        self.osNames     = [] # available OS names
        self.brNames     = [] # available browser names

        for os, browser in c.TEMPLATES.keys(): 

            self.BrowsertoOS[browser].append(os)

            if os not in self.osNames: 
                self.osNames.append(os)
            
            if browser not in self.brNames: 
                self.brNames.append(browser)

        # List of available browsers/OS/platform types
        self.osTypes = list(set(c.OS_TYPES.values()))

        # Parser object
        self.parser = Parser()
        
        return


    def __call__(self, 
        deviceType  : str = 'desktop', # Device type
        browserName : str = None,      # Browser name
        ) -> UserAgent:
        """ Makes the user agent for the given operating system and browser.
            If OS and browser names are not provided, they will be randomly selected.

            Possible selections:
            * device  : desktop/mobile
            * browser : chrome/edge/firefox/safari
        """

        browser = self._makeBrowser(browserName)
        os      = self._makeOS(browser.name, deviceType)

         # Get user agent string
        ua      = UserAgent
        ua.name = self._makeUserAgentName(os, browser)

        # Parse it
        ua.browser, ua.cpu, ua.device, ua.engine, ua.os = self.parser(ua.name) 
        
        # Get User agent hints
        ua.clientHints = CH(ua.browser, ua.cpu, ua.device, ua.os)
        
        return ua


    def _makeBrowser(self, 
        browser: str,   # Name of the selected browser
        ) -> Software:
        """ Makes a browser Software given its name """
        
        if not browser: 
            browser = choice(self.brNames) # Choose one at random if not provided

        else: # Ensure lowercase and availability
            browser = browser.lower()

            if not browser in self.brNames:
                raise ValueError(f'Browser {browser} is not supported')

        return self.browser(browser) # Make Software object


    def _makeOS(self,
        browser: str,   # Name of the selected browser
        device : str,   # Name of the selected device type
        ) -> Software:
        """ Selects and generates an OS that is compatible with the specified
            browser name and device type.
        """

        # Checks if an OS (given its name) is compatible with a given device type
        isDeviceCompatible = lambda osName, deviceType: c.OS_TYPES[osName] == deviceType

        # Get browser compatible OS
        browserCompatible  = self.BrowsertoOS[browser]
        
        # Choose one at random if its also device compatible
        osName = choice(
            [name for name in browserCompatible if isDeviceCompatible(name, device)]
        )

        return self.android() if osName == 'android' else self.os(osName) # Make software object
    

    def _makeUserAgentName(self, 
        os      : Software, # Selected Operating system
        browser : Software  # Selected browser
        ) -> str:
        """ Generates a user agent for the given browser and operating system. """

        # Select a template (if multiples exist)
        agent = choice(c.TEMPLATES[(os.name, browser.name)])
        
        # Replace version(s) details
        for name in self.osNames: agent = agent.replace(f'{{{name}}}', os.version)
        for name in self.brNames: agent = agent.replace(f'{{{name}}}', browser.version)
        
        agent = agent.replace('{webkit}', browser.details.get('webkit', '')).\
                      replace('{device}', '; ' + os.details.get('device_name', '')).\
                      replace('{build}' , '; Build/' + os.details.get('build_number', ''))

        return agent