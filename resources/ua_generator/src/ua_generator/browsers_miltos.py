import random 
from abc import ABC

versions = {
    'chrome' : {    # Source: https://en.wikipedia.org/wiki/Google_Chrome_version_history
        '76.0.3809' :   {'minor_range': (0, 255), 'webkit': '537.36'},
        '77.0.3865' :   {'minor_range': (0, 255), 'webkit': '537.36'},
        '78.0.3904' :   {'minor_range': (0, 255), 'webkit': '537.36'},
        '79.0.3945' :   {'minor_range': (0, 255), 'webkit': '537.36'},
        '80.0.3987' :   {'minor_range': (0, 255), 'webkit': '537.36'},
        '81.0.4044' :   {'minor_range': (0, 255), 'webkit': '537.36'},
        '83.0.4103' :   {'minor_range': (0, 255), 'webkit': '537.36'},
        '84.0.4147' :   {'minor_range': (0, 255), 'webkit': '537.36'},
        '85.0.4183' :   {'minor_range': (0, 255), 'webkit': '537.36'},
        '86.0.4240' :   {'minor_range': (0, 255), 'webkit': '537.36'},
        '87.0.4280' :   {'minor_range': (0, 255), 'webkit': '537.36'},
        '88.0.4324' :   {'minor_range': (0, 255), 'webkit': '537.36'},
        '89.0.4389' :   {'minor_range': (0, 255), 'webkit': '537.36'},
        '90.0.4430' :   {'minor_range': (0, 255), 'webkit': '537.36'},
        '91.0.4472' :   {'minor_range': (0, 255), 'webkit': '537.36'},
        '92.0.4515' :   {'minor_range': (0, 255), 'webkit': '537.36'},
        '93.0.4577' :   {'minor_range': (0, 255), 'webkit': '537.36'},
        '94.0.4606' :   {'minor_range': (0, 255), 'webkit': '537.36'},
        '95.0.4638' :   {'minor_range': (0, 255), 'webkit': '537.36'},
        '96.0.4664' :   {'minor_range': (0, 255), 'webkit': '537.36'},
        '97.0.4692' :   {'minor_range': (0, 255), 'webkit': '537.36'},
        '98.0.4758' :   {'minor_range': (0, 255), 'webkit': '537.36'},
        '99.0.4844' :   {'minor_range': (0, 255), 'webkit': '537.36'},
        '100.0.4896':   {'minor_range': (0, 255), 'webkit': '537.36'},
        '101.0.4951':   {'minor_range': (0, 255), 'webkit': '537.36'},
        '102.0.5005':   {'minor_range': (0, 255), 'webkit': '537.36'},
        '103.0.0'   :   {'minor_range': (0, 255), 'webkit': '537.36'}
    },
    'edge': {       # Source: https://docs.microsoft.com/en-us/deployedge/microsoft-edge-release-schedule
        '88.0.705'  :   {'minor_range': (0, 99), 'webkit': '537.36'},
        '89.0.774'  :   {'minor_range': (0, 99), 'webkit': '537.36'},
        '90.0.818'  :   {'minor_range': (0, 99), 'webkit': '537.36'},
        '91.0.864'  :   {'minor_range': (0, 99), 'webkit': '537.36'},
        '92.0.902'  :   {'minor_range': (0, 99), 'webkit': '537.36'},
        '93.0.961'  :   {'minor_range': (0, 99), 'webkit': '537.36'},
        '94.0.992'  :   {'minor_range': (0, 99), 'webkit': '537.36'},
        '95.0.1020' :   {'minor_range': (0, 99), 'webkit': '537.36'},
        '96.0.1054' :   {'minor_range': (0, 99), 'webkit': '537.36'},
        '97.0.1072' :   {'minor_range': (0, 99), 'webkit': '537.36'},
        '98.0.1108' :   {'minor_range': (0, 99), 'webkit': '537.36'},
        '99.0.1141' :   {'minor_range': (0, 99), 'webkit': '537.36'},
        '99.0.1146' :   {'minor_range': (0, 99), 'webkit': '537.36'},
        '100.0.1185':   {'minor_range': (0, 99), 'webkit': '537.36'},
        '101.0.1210':   {'minor_range': (0, 99), 'webkit': '537.36'},
        '102.0.1245':   {'minor_range': (0, 99), 'webkit': '537.36'},
        '103.0.1264':   {'minor_range': (0, 99), 'webkit': '537.36'},
        '104.0.1293':   {'minor_range': (0, 99), 'webkit': '537.36'},
        '105.0.1146':   {'minor_range': (0, 99), 'webkit': '537.36'},
        '106.0.1146':   {'minor_range': (0, 99), 'webkit': '537.36'}
    },
    'firefox': {    # Source: https://en.wikipedia.org/wiki/Firefox_version_history
        '78'    :   {'minor_range': (0, 15)},
        '79'    :   {'minor_range': (0, 0)},
        '80'    :   {'minor_range': (0, 1)},
        '81'    :   {'minor_range': (0, 2)},
        '82'    :   {'minor_range': (0, 3)},
        '83'    :   {'minor_range': (0, 0)},
        '84'    :   {'minor_range': (0, 2)},
        '85'    :   {'minor_range': (0, 2)},
        '86'    :   {'minor_range': (0, 1)},
        '87'    :   {'minor_range': (0, 0)},
        '88'    :   {'minor_range': (0, 1)},
        '89'    :   {'minor_range': (0, 2)},
        '90'    :   {'minor_range': (0, 2)},
        '91.0'  :   {'minor_range': (0, 13)},
        '92.0'  :   {'minor_range': (0, 1)},
        '93.0'  :   {'minor_range': (0, 0)},
        '94.0'  :   {'minor_range': (0, 2)},
        '95.0'  :   {'minor_range': (0, 2)},
        '96.0'  :   {'minor_range': (0, 3)},
        '97.0'  :   {'minor_range': (0, 2)},
        '98.0'  :   {'minor_range': (0, 2)},
        '99.0'  :   {'minor_range': (0, 1)},
        '100.0' :   {'minor_range': (0, 2)},
        '101.0' :   {'minor_range': (0, 1)},
        '102.0' :   {'minor_range': (0, 6)},
        '103.0' :   {'minor_range': (0, 2)}
    },
    'safari' : {    # Source: https://en.wikipedia.org/wiki/Safari_version_history
        '8'         :   {'minor_range': (0, 0), 'webkit': '600.5.17'},
        '9'         :   {'minor_range': (0, 0), 'webkit': '601.1.46'},
        '10'        :   {'minor_range': (0, 0), 'webkit': '602.4.8'},
        '11'        :   {'minor_range': (0, 0), 'webkit': '604.1.38'},
        '12'        :   {'minor_range': (0, 1), 'webkit': '605.1.15'},
        '13'        :   {'minor_range': (0, 1), 'webkit': '605.1.15'},
        '14'        :   {'minor_range': (0, 1), 'webkit': '605.1.15'},
        '15'        :   {'minor_range': (0, 5), 'webkit': '605.1.15'},
    },
    'ios' : { # Source: # https://en.wikipedia.org/wiki/IOS_version_history
        '9': {'minor_range': (0, 3)},
        '10': {'minor_range': (0, 3)},
        '11': {'minor_range': (0, 4)},
        '12': {'minor_range': (0, 5)},
        '13': {'minor_range': (0, 7)},
        '14': {'minor_range': (0, 8)},
        '15': {'minor_range': (0, 6)},
    },
    'linux': { # Source: https://en.wikipedia.org/wiki/Linux_kernel_version_history
        '5.0': {'minor_range': (0, 21)},
        '5.1': {'minor_range': (0, 21)},
        '5.2': {'minor_range': (0, 20)},
        '5.3': {'minor_range': (0, 18)},
        '5.4': {'minor_range': (0, 184)},
        '5.5': {'minor_range': (0, 19)},
        '5.6': {'minor_range': (0, 19)},
        '5.7': {'minor_range': (0, 19)},
        '5.8': {'minor_range': (0, 18)},
        '5.9': {'minor_range': (0, 16)},
        '5.10': {'minor_range': (0, 105)},
        '5.11': {'minor_range': (0, 22)},
        '5.12': {'minor_range': (0, 19)},
        '5.13': {'minor_range': (0, 19)},
        '5.14': {'minor_range': (0, 21)},
        '5.15': {'minor_range': (0, 28)},
        '5.16': {'minor_range': (0, 14)},
        '5.17': {'minor_range': (0, 11)},
        '5.18': {'minor_range': (0, 16)},
        '5.19': {'minor_range': (0, 1)},
    },
    'macos': { # https://en.wikipedia.org/wiki/MacOS_version_history
            '10.8': {'minor_range': (0, 8)},
            '10.9': {'minor_range': (0, 5)},
            '10.10': {'minor_range': (0, 5)},
            '10.11': {'minor_range': (0, 6)},
            '10.12': {'minor_range': (0, 6)},
            '10.13': {'minor_range': (0, 6)},
            '10.14': {'minor_range': (0, 6)},
            '10.15': {'minor_range': (0, 7)},
            '11.0': {'minor_range': (0, 0)},
            '11.2': {'minor_range': (0, 3)},
            '11.3': {'minor_range': (0, 1)},
            '11.5': {'minor_range': (0, 2)},
            '11.6': {'minor_range': (0, 6)},
            '12.0': {'minor_range': (0, 1)},
            '12.2': {'minor_range': (0, 1)},
            '12.3': {'minor_range': (0, 1)},
            '12.4': {'minor_range': (0, 0)},
            '12.5': {'minor_range': (0, 1)},
    },
    'windows' : {
        '6.1',
        '6.2',
        '6.3',
        '10.0'
    }
}

class Item():
    """ Abstract Browser class. Defines necessary methods """

    def __init__(self, name: str):
        """ Loads the version history corresponding to the browser """

        if name in versions:
            self.versions = versions[name]

            if isinstance(self.versions, set):
                self.versions = tuple(self.versions)
        
        else:
            raise NotImplementedError(f'Platform {name} is not supported')

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

if __name__ == '__main__':

    browser = Item('edge')

    for _ in range(10):
        print(browser.version())