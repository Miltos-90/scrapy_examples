from ua_parser import Parser
from ua_generator import Generator
from ua_scraper import Scraper
from ua_client_hints import ClientHints as CH
import os


def readFile(filename: str) -> list:
    """ Generic txt reader. """

    if not os.path.isfile(filename):
        raise FileNotFoundError(f'File {filename} does not exist.')
    
    with open(filename, 'r') as f:
        x = f.readlines()       # read into a list
    x = [e.strip()for e in x]   # Remove leading/trailing spaces

    return x

# TODO: Update generator with latest versions. Limit old versions as well!
# TODO: Scraper, parser, and generator Singletons to new module utils.

if __name__ == '__main__':
    
    uaStrings = readFile('user_agents.txt')
    
    G = Generator()
    P = Parser()
    #S = Scraper()

    # Scraped user agents
    #for _ in range(10): print(S())

    # Generate user agents
    for _ in range(250):
        ggg = G() 
        
        break

    # Parser 
    for i, s in enumerate(uaStrings):

        d = P(s)

        print(s)
        for k, v in d.items():
            pass
            print(k, v)

        # Make client hints
        chDict = CH(d)
        print(chDict)

        if i == 137:
            break


    
    