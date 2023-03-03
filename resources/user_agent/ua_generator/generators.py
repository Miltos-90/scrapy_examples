""" This module implements the user agent generator, that provides fake user agents for 
    the browsers and operating systems defined in the user_agent_sim_data file.

    Based on the work of: https://github.com/iamdual/ua-generator/
"""

from random       import randint, choice
from ua_generator import constants
from dataclasses  import dataclass
from collections  import defaultdict
import string

@dataclass
class Software():
    """ Holds properties for a single Software object. """
    name    : str  = None
    version : str  = None
    details : dict = None


class SoftwareGenerator():
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

        if not SoftwareGenerator._skipMinorVersion(name, minorVer): 
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


class AndroidOSGenerator(SoftwareGenerator):
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
        os = super(AndroidOSGenerator, self).__call__(brand)
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


class Generator():
    """ Generates a randomly-selected user agent according to a set type, OS, and browser """

    def __init__(self,
        osTypeDict  : dict = constants.OS_TYPES,    # Dictionary with <os>:<type>
        osVersions  : dict = constants.OS,          # Data for the operating systems
        brVersions  : dict = constants.BROWSERS,    # Data for the browsers
        uaTemplates : dict = constants.TEMPLATES,   # User agent templates
        androidSys  : dict = {                      # Data for Android devices
            'versions' : constants.android.VERSIONS,
            'devices'  : constants.android.DEVICES
        }
    ):

        # Instantiate generators
        self.os      = SoftwareGenerator(osVersions)
        self.android = AndroidOSGenerator(androidSys)
        self.browser = SoftwareGenerator(brVersions)
        

        # List of valid OS/browser combinations
        self.browsersPerOS  = defaultdict(list)
        for os, browser in uaTemplates.keys(): 
            self.browsersPerOS[os].append(browser)

        # List of available browsers/OS/platform types
        self.osNames = list(self.browsersPerOS.keys())
        self.brNames = list(brVersions.keys())
        self.osTypes = list(set(osTypeDict.values()))
        self.osDict  = osTypeDict
        
        # User agent templates
        self.templates = uaTemplates

        return


    def __call__(self, 
        device  : str = None, # Device type
        os      : str = None, # OS name
        browser : str = None  # Browser name
        ) -> str:
        """ Makes the user agent for the given operating system and browser.
            If OS and browser names are not provided, they will be randomly selected.

            Possible selections:
            * device  : desktop/mobile
            * os      : windows/macos/ios/linux/android
            * browser : chrome/edge/firefox/safari
        """

        # Lowercase all 
        if os      : os = os.lower()
        if browser : browser = browser.lower()

        device  = self._checkDeviceType(device, os)
        os      = self._makeOS(device, os)
        browser = self._makeBrowser(os.name, browser)
        
        return self._makeUserAgent(os, browser)


    def _checkDeviceType(self, 
        device: str, # Device type      : mobile, desktop
        osName: str  # Operating system : windows, macos, ios, linux, android
        ) -> str:
        """ Selects/validates specified device type. """

        if device is None and osName is None: 
            _type = choice(self.osTypes) # Nothing is specified. Set randomly

        elif osName is not None:             
            _type = self.osDict[osName] # OS is specified. Set matching type.

        elif device not in self.osTypes:      
            raise NotImplementedError('Unsupported device type') # Invalid type.

        return _type


    def _makeBrowser(self,
        osName : str = None, # Operating system : windows, macos, ios, linux, android
        brName : str = None  # Browser          : chrome, edge, firefox, safari
        ) -> Software:
        """ Chooses randomly a user of the appropriate type if OS and browser are not specified """
        
        # Grab an appropriate browser if not specified
        if brName is None:
            brName = choice(self.browsersPerOS[osName])

        elif brName not in self.browsersPerOS[osName]:
            msg = f'Browser {brName.title()} is not supported by OS {osName.title()}.'
            raise ValueError(msg)

        return self.browser(brName)


    def _makeOS(self,
        device: str, # Device type to be selected
        osName: str  # Name of the OS to be selected
        ) -> Software:
        """ Selects/validates specified OS """

        # Get an OS of the selected type if not specified by the user
        availableOS = [osName for osName, osType in self.osDict.items() if osType == device] 

        if osName is None: 
            osName = choice(availableOS)
        
        elif osName not in availableOS:
            msg = f'Operating system {osName.title()} is not of type {device.title()}.'
            raise ValueError(msg)

        return self.android() if osName == 'android' else self.os(osName)


    def _makeUserAgent(self, 
        os      : Software, # Selected Operating system
        browser : Software  # Selected browser
        ) -> str:
        """ Generates a user agent for the given browser and operating system. """

        # Select a template (if multiples exist)
        agent = choice(self.templates[(os.name, browser.name)])
        
        # Replace version(s) details
        for name in self.osNames: agent = agent.replace(f'{{{name}}}', os.version)
        for name in self.brNames: agent = agent.replace(f'{{{name}}}', browser.version)
        
        agent = agent.replace('{webkit}', browser.details.get('webkit', '')).\
                      replace('{device}', '; ' + os.details.get('device_name', '')).\
                      replace('{build}' , '; Build/' + os.details.get('build_number', ''))

        return agent