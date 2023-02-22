from random import randint, choice
import software_data as data
import string


class SoftwareGenerator():

    def __init__(self, versions):
        
        self.versionData = versions
        self.versions    = list(versions.keys())


    def __call__(self, name):
        
        versions = self.versionData[name]  # Get versions relevant to software <name>

        # if only keys are specified (i.e. the structure is a set, convert to dict)
        if isinstance(versions, set): 
            versions = dict.fromkeys(versions, {})

        # Select a version from those
        major   = choice(list(versions.keys()))  
        details = versions[major]

        return self.makeDetails(major, details)


    @staticmethod
    def makeDetails(key, props):

        d = {'major': key}
        for propKey, propValue in props.items():
                    
            if propKey == 'minor_range': 
                d['minor'] = randint(propValue[0], propValue[1])
            else:
                d[propKey] = propValue

        return d

class BrowserGenerator(SoftwareGenerator):

    def __init__(self):

        super().__init__(data.browsers)
        self.names = list(data.browsers.keys())

    def __call__(self, name): 

        return super(BrowserGenerator, self).__call__(name)
 

# TODO: Do you need systems in here or on the platrform generator?
class OperatingSystemGenerator(SoftwareGenerator):

    def __init__(self, 
        versions : dict = data.operating_systems,
        systems  : list = list(data.operating_systems.keys())
        ):

        super().__init__(versions)
        self.names = systems

    def __call__(self, name):

        return super(OperatingSystemGenerator, self).__call__(name)

# TODO: Do you need brands in here or on the platform generator?. You do, w/ fefault values. But not on the generic OS generator
class AndroidOSGenerator(OperatingSystemGenerator):

    def __init__(self, 
        brands   : list = list(data.android.versions.keys()), 
        versions : dict = data.android.versions, 
        devices  : dict = data.android.devices):
        
        super().__init__(versions, brands)
        self.devices  = devices

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

    def __init__(self):
        self.os        = OperatingSystemGenerator()
        self.androidOs = AndroidOSGenerator()
        self.browser   = BrowserGenerator()
        self.osList    = self.os.names + ['android']
        self.browserList = self.browser.names

    def __call__(self, osName:str = None, brName: str = None):

        if osName is None : osName = choice(self.osList)
        if brName is None : brName = choice(self.browserList)

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

    for _ in range(5):
        
        p = pg()
        print(p.os['name'], p.os['version'])
        print(p.browser['name'], p.browser['version'])
        print()

