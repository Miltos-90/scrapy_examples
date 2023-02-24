""" This module implements the user agent generator, that provides fake user agents for 
    the browsers and operating systems defined in the user_agent_sim_data file.
"""

from random import randint, choice
import user_agent_sim_data as data
import string
from dataclasses import dataclass
from collections import defaultdict
from abc import ABCMeta


class Singleton(ABCMeta):
    """ Singleton metaclass """
    _instances = {}

    def __call__(cls, *args, **kwargs):

        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]


@dataclass
class Software():
    """ Holds properties for a single Software object. """
    name    : str  = None
    version : str  = None
    details : dict = None


class SoftwareGenerator():
    """ Generic software generator. It provides random software versions
        and their corresponding details
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


class UserAgentGenerator(metaclass = Singleton):
    """ Generates a random OS and a browser. """

    def __init__(self,
        osVersions  : dict = data.operating_systems, # Data for the operating systems
        brVersions  : dict = data.browsers,          # Data for the browsers
        uaTemplates : dict = data.templates,         # User agent templates
        androidSys  : dict = {                       # Data for the Android devices
            'versions' : data.android.versions,
            'devices'  : data.android.devices
        }
    ):

        # Instantiate generators
        self.os      = SoftwareGenerator(osVersions)
        self.android = AndroidOSGenerator(androidSys)
        self.browser = SoftwareGenerator(brVersions)

        # List of valid OS/browser combinations
        self.combos  = defaultdict(list)
        for os, browser in uaTemplates.keys(): 
            self.combos[os].append(browser)

        # List of available browsers and OS
        self.osNames = list(self.combos.keys())
        self.brNames = list(brVersions.keys())
        
        # User agent templates
        self.templates = uaTemplates

        return


    def __call__(self, 
        osName : str = None,    # Operating system name
        brName : str = None     # Browser name
        ) -> str:
        """ Makes the user agent for the given operating system and browser.
            If OS and browser names are not provided, they will be randomly selected.
        """

        # If browser/os name is not provided, pick one at random
        if osName is None: osName = choice(self.osNames)
        if brName is None: brName = choice(self.combos[osName])

        # Make browser and operating system
        os      = self.android() if osName == 'android' else self.os(osName)
        browser = self.browser(brName)

        # Select a template (if multiples exist)
        agent = choice(self.templates[(os.name, browser.name)])
        
        # Replace version details
        for name in self.osNames: agent = agent.replace(f'{{{name}}}', os.version)
        for name in self.brNames: agent = agent.replace(f'{{{name}}}', browser.version)
        
        agent = agent.replace('{webkit}', browser.details.get('webkit', '')).\
                      replace('{device}', '; ' + os.details.get('device_name', '')).\
                      replace('{build}' , '; Build/' + os.details.get('build_number', ''))
        
        return agent


if __name__ == '__main__':

    pg = UserAgentGenerator()
    for _ in range(250):
        
        p = pg()
        print(p)