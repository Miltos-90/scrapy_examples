import random
import software_data

class Software():
    """ Abstract Browser class. Defines necessary methods """

    def __init__(self, name: str,  versionDict : dict):
        """ Loads the version history corresponding to the browser """

        name = name.lower()
        if name in versionDict: 
            self.versions = versionDict[name]

            if isinstance(self.versions, set): 
                self.versions = tuple(self.versions)
        
        else: 
            raise NotImplementedError(f'Software {name} is not a supported')

        return

    def version(self):
        """ Returns a random version for a given browser.
        """

        choice = random.randint(0, len(self.versions) - 1)
        i = 0

        if isinstance(self.versions, dict):
            for major, props in self.versions.items():
                if choice == i:
                    minor = random.randint(int(props['minor_range'][0]), int(props['minor_range'][1]))

                    if 'webkit' in props: # i.e. Chrome, Edge, and Safari
                        return {'major': major, 'minor': minor, 'webkit': props['webkit']}
                    else:                 # i.e. Firefox
                        return {'major': major, 'minor': minor}
                i = i + 1
        else:
            return {'major': random.choice(self.versions)}

Browser           = lambda name: Software(name, versionDict = software_data.browsers.versions)
OperatingSystem   = lambda name: Software(name, versionDict = software_data.operating_systems.versions)

if __name__ == '__main__':

    n = 'Linux'
    b = OperatingSystem(n)
    for _ in range(10):
        print(n, b.version())

    n = 'safari'
    b = Browser(n)
    for _ in range(10):
        print(n, b.version())