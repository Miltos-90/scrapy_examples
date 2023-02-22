from random import randint, choice
import software_data as data
import string


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

    def __init__(self, systems: dict):
        
        super().__init__(systems['versions'])
        self.devices = systems['devices']

        return

    def __call__(self, brand: str = None):

        brand = choice(self.names)
        os    = super(AndroidOSGenerator, self).__call__(brand)

        # Make Android-specific details
        os['build_number'] = self._buildNumber(brand, os['build_number'])
        os['device_name']  = choice(self.devices[brand])

        return os
    
    @staticmethod
    def _buildNumber(brand, buildStr): 

        bNo = choice(buildStr)

        if brand == 'nexus' or brand == 'samsung':
            bNo = bNo.replace(
                '{s}', 
                '{}'.format(choice(string.ascii_uppercase)))

        bNo = bNo.\
            replace(
                '{d}',
                '{:02d}{:02d}{:02d}'.format(randint(17, 22), randint(0, 12), randint(0, 29))).\
            replace(
                '{v}', 
                '{}'.format(randint(1, 255)))

        return bNo


class PlatformGenerator():

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
            
        self.osNames = self.os.names + ['android']
        self.brNames = self.browser.names
        

    def __call__(self, osName:str = None, brName: str = None):

        if osName is None : osName = choice(self.osNames)
        if brName is None : brName = choice(self.brNames)

        if osName != 'android':
            os = {'name': osName, 'version': self.os(osName)}
        else:
            os = {'name': osName, 'version': self.androidOs()}

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

