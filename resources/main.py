""" HTTP header generator. 
    Based on the repo: https://github.com/MichaelTatarski/fake-http-header

"""

# TODO Fix header order
# TODO Make header compatibility for each header and browser: (chrome/edge/firefox/safari for generator +mozilla/opera for scraper)
# TODO  Check when DNT and Upgrade-insecure-requests should be included (browser/version combo) as above
# TODO Check this: https://github.com/AhmedSakrr/Fake-Headers
# TODO User agent integration with scrapy: https://gist.github.com/seagatesoft/e7de4e3878035726731d

from user_agent import Generator
from utils      import *
from utils      import Singleton
import random as rd


class GenericHeaderGenerator(metaclass = Singleton):

    def __init__(self):

        f = './data/common_agents.txt'
        #self.UserAgent  = Generator(by = 'program')
        self.UserAgent  = Generator(by = 'file', filename = f)
        self.Referer    = HTTPHeaderGenerator('./data/referers.json')
        self.Encoder    = AcceptEncoding('./data/acceptEncoding.json')
        self.Language   = AcceptLanguage('./data/languages.json')
        self.Accept     = HTTPHeaderGenerator('./data/accept.json')
        self.domains    = list(self.Referer.data.keys())

        return

    def __call__(self) -> dict:

        """ Generates realistic, randomly-chosen HTTP headers.
        Inputs: 
            * domain (list) can be either:
                * Empty: random selection among all
                * list containing one or more of: 
                    .com, .jsp, .edu, .org, .info, .net, .php3, .aspx, .biz, .uk,  .it,
                    .is,  .ua,  .cc,  .de,  .us,   .tv,  .eu, .ru, .cn, .jp, .nl, .be,  
                    .fr,  .ch,  .gr,  .se,   .dk,  .bg,  .cz, .hu, .lt, .pl, .ro, .sk, 
                    .si,  .br,  .pt,  .es,  .il,   .au,  .io,   .no,   .ir, .at
            * Browser (list) can be either
                * Empty: random selection among all
                * list containing one or more of: 
                    chrome, edge, firefox, safari
        """

        
        # Get a random domain and user agent
        userAgent = self.UserAgent()
        domain    = rd.choice(self.domains)
        bName     = userAgent.browser.get('name').lower()            

        headers = {
            "User-Agent"      : userAgent.name,
            "Referer"         : self.Referer(domain, defaultKey = 'com'), 
            "Accept"          : self.Accept(bName, defaultKey = 'chrome'),
            "Accept-Language" : self.Language(domain),
            "Accept-Encoding" : self.Encoder(),
            "DNT"             : "1", 
            "Upgrade-insecure-requests": "1",
            }

        #print(userAgent.clientHints)

        # Get browser version (and convert it to integer)
        bVersion = int(userAgent.browser.get('majorVersion', 0))

        # Add fixed headers if needed. This is wrong. Check: 
        hasSecFetch = \
            (bName == 'chrome' and bVersion >= 76) or \
            (bName == 'firefox' and bVersion >= 90) or \
            (bName == 'edge' and bVersion >= 79)

        #print(bName, bVersion, hasSecFetch)

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
    
    for _ in range(100):

        h = headers()
        for k, v in h.items():
            
            print(f'{k}: {v}')


