from random import randint, choice
import software_data as data
import string

""" TODO
Make software object which contains name/version/details fields.
Have the software generators return a software

"""


class SoftwareGenerator():
    """ Generic software generator. It provides random software versions
        and their corresponding details
    """

    def __init__(self, versions):
        
        self.versions = versions
        self.names    = list(versions.keys())
        return


    def __call__(self, name: str) -> dict:
        """ Randomly choose a software version and its associated details"""
        
        versions = self.versions[name] # Get versions relevant to software <name>

        # if only keys are specified in the data (i.e. the structure is a set), convert to dict
        if isinstance(versions, set): 
            versions = dict.fromkeys(versions, {})

        # Select a version from those
        majorVer = choice(list(versions.keys()))  
        details  = versions[majorVer]

        return self.makeDetails(majorVer, details)


    @staticmethod
    def makeDetails(key, props):
        """ Generates all addditional details of a major version of a software """

        d = {'major': key} # Add major version to the dict

        # Loop over all properties and populate dictionary
        for propKey, propValue in props.items():
                    
            if propKey == 'minor_range': 
                d['minor'] = randint(propValue[0], propValue[1])
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
        os = super(AndroidOSGenerator, self).__call__(brand)

        # Make Android-specific details
        os['build_number'] = self._buildNumber(os['build_number'])
        os['device_name']  = choice(self.devices[brand])

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


class PlatformGenerator():
    """ Generates a random OS and a browser. """

    def __init__(self,
        osVersions : dict = data.operating_systems,
        brVersions : dict = data.browsers,
        androidSys : dict = {
            'versions' : data.android.versions,
            'devices'  : data.android.devices
        }
    ):

        self.os        = SoftwareGenerator(osVersions)
        self.browser   = SoftwareGenerator(brVersions)
        self.androidOs = AndroidOSGenerator(androidSys)
        
        # List of OS and browsers available
        self.osNames = self.os.names + ['android']
        self.brNames = self.browser.names
        

    def __call__(self, osName:str = None, brName: str = None):
        """ Either returns an an OS and a browser  with the given 
            names or chooses both at random
        """

        if osName is None: osName = choice(self.osNames)

        if osName != 'android' : os = {'name': osName, 'version': self.os(osName)}
        else                   : os = {'name': osName, 'version': self.androidOs()}

        if brName is None: brName = choice(self.brNames)
        browser = {'name': brName, 'version': self.browser(brName)}

        return Platform(os, browser)


class Platform():

    def __init__(self, os, browser):
        self.os        = os
        self.browser   = browser
        

if __name__ == '__main__':

    pg = PlatformGenerator()

    for _ in range(50):
        
        p = pg()
        print(p.os['name'], p.os['version'])
        print(p.browser['name'], p.browser['version'])
        print()

