from random import randint, choice
import software_data as data
import string


class VersionGenerator():

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

class BrowserGenerator():

    def __init__(self):

        self.names    = list(data.browsers.keys())
        self.versions = VersionGenerator(data.browsers)

    def __call__(self, name): 
        return self.versions(name)

class AndroidOSGenerator():

    def __init__(self):
        
        self.brands   = list(data.android.versions.keys())
        self.versions = VersionGenerator(data.android.versions)
        self.devices  = data.android.devices

        return

    def __call__(self):

        brand = choice(self.brands)
        os    = self.versions(brand)
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

class OperatingSystemGenerator():

    def __init__(self):

        self.names     = list(data.operating_systems.keys())
        self.names.append('android')
        self.versions  = VersionGenerator(data.operating_systems)
        self.androidOS = AndroidOSGenerator()

    def __call__(self, name):

        if name == 'android': return self.androidOS()
        else                : return self.versions(name)

class PlatformGenerator():

    def __init__(self):
        self.os      = OperatingSystemGenerator()
        self.browser = BrowserGenerator()

    def __call__(self, osName:str = None, brName: str = None):

        if osName is None : osName = choice(self.os.names)
        if brName is None : brName = choice(self.browser.names)

        os      = {'name': osName, 'version': self.os(osName)}
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

