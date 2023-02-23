from random import randint, choice
import software_data as data
import string
from dataclasses import dataclass

@dataclass
class Software():
    name    : str  = None
    version : str  = None
    details : dict = None

@dataclass
class User():
    browser : Software = None
    os      : Software = None


class SoftwareGenerator():
    """ Generic software generator. It provides random software versions
        and their corresponding details
    """

    def __init__(self, versions):
        
        self.versions = versions
        self.names    = list(versions.keys())
        return


    def __call__(self, name: str) -> Software:
        """ Randomly choose a software version and its associated details"""
        
        versions = self.versions[name] # Get versions relevant to software <name>

        # if only keys are specified in the data (i.e. the structure is a set), convert to dict
        if isinstance(versions, set): 
            versions = dict.fromkeys(versions, {})

        # Select a version from those
        majorVer = choice(list(versions.keys()))  

        return Software(
            name    = name,
            version = majorVer,
            details = self.makeDetails(versions[majorVer])
        )


    @staticmethod
    def makeDetails(props):
        """ Generates all addditional details of a major version of a software """

        # Loop over all properties and populate dictionary
        d = {}
        for propKey, propValue in props.items():
                    
            if propKey == 'minor_range': 
                d['minor_version'] = randint(propValue[0], propValue[1])
            else:
                d[propKey] = propValue

        return d


class AndroidOSGenerator(SoftwareGenerator):
    """ Generic Android OS generator. """

    def __init__(self, systems: dict):
        
        super().__init__(systems['versions'])
        self.devices = systems['devices']

        return

    def __call__(self, brand: str = None) -> dict:
        """ Generate a random Android OS """

        # Randomly select a brand of mobile phones operating on Android and make OS
        if brand is None: brand = choice(self.names)
        
        os      = super(AndroidOSGenerator, self).__call__(brand)
        os.name = 'android'

        # Make Android-specific details
        
        os.details['brand']        = brand
        os.details['build_number'] = self._buildNumber(os.details['build_number'])
        os.details['device_name']  = choice(self.devices[brand])

        return os
    

    @staticmethod
    def _buildNumber(buildNumbers : tuple) -> str:
        """ Formats the buildnumber according to the mmanufacturer. 
            Supports nexus, samsung and pixel devices.
        """

        buildNum   = choice(buildNumbers) # Choose a build number at random
        formatters = AndroidOSGenerator._makeFormatters()

        for f in formatters: 
            buildNum = buildNum.replace(f['from'], f['to'])

        return buildNum


    @staticmethod
    def _makeFormatters() -> tuple:
        """ Generates appropriate formatters for the build number of an Android device. """

        return (
            {'from': '{s}', 'to' : '{}'.format(choice(string.ascii_uppercase))},
            {'from': '{d}', 'to' : '{:02d}{:02d}{:02d}'.format(randint(17, 22), randint(0, 12), randint(0, 29))},
            {'from': '{v}', 'to' : '{}'.format(randint(1, 255))}
        )


class UserGenerator():
    """ Generates a random OS and a browser. """

    def __init__(self,
        osVersions  : dict = data.operating_systems,
        brVersions  : dict = data.browsers,
        uaTemplates : dict = data.templates,
        androidSys  : dict = {
            'versions' : data.android.versions,
            'devices'  : data.android.devices
        }
    ):

        self.os        = SoftwareGenerator(osVersions)
        self.androidOs = AndroidOSGenerator(androidSys)
        self.browser   = SoftwareGenerator(brVersions)
        
        # List of OS and browsers available
        self.combinations = self._validCombinations(uaTemplates)
        self.osNames      = list(self.combinations.keys())
        
        # User agent templates
        self.templates = uaTemplates

        return

    def __call__(self, osName:str = None, brName: str = None) -> User:
        """ Either returns an an OS and a browser  with the given 
            names or chooses both at random
        """

        if osName is None: osName = choice(self.osNames)
        if brName is None: brName = choice(self.combinations[osName])

        user = User(os = self._makeOS(osName), browser = self.browser(brName))
        
        self._makeAgent(user)

        return user

    def _makeOS(self, name) -> Software:
        """ Generates an operating system given its name. """

        return self.androidOs() if name == 'android' else self.os(name)

    def _makeAgent(self, user: User):

        # Select a template (if multiples exist)
        template = choice(self.templates[(user.os.name, user.browser.name)])

        # Replace os version
        template = template.replace('{windows}', user.os.version)
        template = template.replace('{linux}', user.os.version)
        template = template.replace('{android}', user.os.version.replace('.0', ''))
        template = template.replace('{macos}', version(user.os, strip_zero = True).replace('.', '_'))
        template = template.replace('{ios}', version(user.os, strip_zero = True).replace('.', '_'))
                
        # Replace browser version
        template = template.replace('{chrome}',  version(user.browser))
        template = template.replace('{firefox}', version(user.browser, strip_zero = True))
        template = template.replace('{safari}', version(user.browser))

        # Replace version details
        template = template.replace('{webkit}', user.browser.details.get('webkit', ''))
        template = template.replace('{device}', '; ' + user.os.details.get('device_name', ''))
        template = template.replace('{build}', '; Build/' + user.os.details.get('build_number', ''))
        
        
        print(template)

        return
        


    @staticmethod
    def _validCombinations(templates):
        """ Generates a dictionary with valid os and browser combinations.
            key: operating system, value: list with valid browsers
        """

        d = {}
        for os, browser in templates.keys():

            if os not in d: 
                d[os] = [] # Make an empty list

            else:           
                d[os].append(browser) # Append

        return d


def version(os, strip_zero=False):

    minorVersion = os.details.get('minor_version')
    
    c = minorVersion and (not strip_zero or (strip_zero and minorVersion > 0) )

    v_str = str(os.version)
    if c:
        v_str += '.' + str(minorVersion)

    return v_str


def major_version(version_dict):
    return str(version_dict['major']).split('.', 1)[0]


if __name__ == '__main__':

    pg = UserGenerator()

    for _ in range(50):
        
        p = pg()
        print(p.os)
        print(p.browser)
        print()

