

from ua_parser import Parser
from ua_generator import Generator
import client_hints as ch
import os


def readFile(filename: str) -> list:
    """ Generic txt reader. """

    if not os.path.isfile(filename):
        raise FileNotFoundError(f'File {filename} does not exist.')
    
    with open(filename, 'r') as f:
        x = f.readlines()       # read into a list
    x = [e.strip()for e in x]   # Remove leading/trailing spaces

    return x


if __name__ == '__main__':
    
    uaStrings = readFile('user_agents.txt')

    G = Generator()
    P = Parser()
    for _ in range(250):
        ggg = G()
        #print(ggg)
        break


for i, s in enumerate(uaStrings):

    d = P(s)

    #print(s)
    for k, v in d.items():
        pass
        #print(k, v)

    if i == 137:
        break

# Make client hints
# TODO: Check bitness
# TODO: Return according to compatibility: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers
# TODO: Clean up UA scraper
chDict = {
    'Sec-CH-UA'                   : ch.UA(d['browser', 'name'], d['browser', 'major_version']),
    'Sec-CH-UA-Full-Version-List' : ch.UA(d['browser', 'name'], d['browser', 'version'],fullVersion = True),
    'Sec-CH-UA-Platform-Version'  : ch.UAPlatformVersion(d['os', 'version']),
    'Sec-CH-UA-Platform'          : ch.UAPlatform(d['os','name']),
    'Sec-CH-UA-Platform'          : ch.UAPlatform(d['os','name']),
    'Sec-CH-UA-Mobile'            : ch.UAMobile(d['device','type']),
    'Sec-CH-UA-Model'             : ch.UAModel(d['device','model']),
    'Sec-CH-UA-Arch'              : ch.UAArch(d['cpu','architecture'])
}

print(chDict)