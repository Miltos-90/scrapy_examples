# TODO Fix header order
# TODO Make header compatibility
# TODO Check when DNT and Upgrade-insecure-requests should be included (browser/version combo)
# TODO User agent integration with scrapy: https://gist.github.com/seagatesoft/e7de4e3878035726731d


from user_agent import Factory as UAF
from abc        import ABCMeta
from utils      import *
import random as rd


class Singleton(ABCMeta):
    """ Singleton metaclass """
    _instances = {}

    def __call__(cls, *args, **kwargs):

        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]


class GenericHeaderGenerator(HTTPHeaderGenerator, metaclass = Singleton):

    def __init__(self):

        self.UserAgent  = UAF(by = 'generator')
        self.Referer    = HTTPHeaderGenerator('./data/referers.json')
        self.Encoder    = AcceptEncoding('./data/acceptEncoding.json')
        self.Language   = AcceptLanguage('./data/languages.json')
        self.Accept     = Accept('./data/accept.json')
        self.domains    = list(self.Referer.data.keys())

        return

    def __call__(self) -> dict:

        """ Generates realistic, randomly-chosen HTTP headers. """
        
        # Get a random domain and user agent
        userAgent = self.UserAgent()
        domain    = rd.choice(self.domains)
        bName     = userAgent.browser.get('name').lower()            

        headers = {
            "User-Agent"      : userAgent.name,
            "Referer"         : self.Referer(domain), 
            "Accept"          : self.Accept(bName),
            "Accept-Language" : self.Language(domain),
            "Accept-Encoding" : self.Encoder(),
            "DNT"             : "1", 
            "Upgrade-insecure-requests": "1",
            }

        # Get browser version (and convert it to integer)
        bVersion = userAgent.browser.get('majorVersion')
        if bVersion: bVersion = int(bVersion)

        # Add fixed headers if needed. This is wrong. Check: 
        hasSecFetch = \
            (bName == 'chrome' and bVersion >= 76) or \
            (bName == 'firefox' and bVersion >= 90) or \
            (bName == 'edge' and bVersion >= 79)

        print(bName, bVersion, hasSecFetch)

        secFetch = { # No need to change those
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
        }

        # Add client hints

        # Order headers accordingly
        

        return headers


if __name__ == "__main__":
    
    headers = GenericHeaderGenerator()
    
    for _ in range(1):

        h = headers()
        #for k, v in h.items():
        #    print(f'{k}: {v}')
