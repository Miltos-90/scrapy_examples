""" HTTP header generator. 
    Partially based on the repo: https://github.com/MichaelTatarski/fake-http-header

"""
# TODO Fix header order (and source on the md file)
# TODO: Fix typehints
# TODO: Cleanup generator.py -> _makeAgent()
# TODO: Check why empty headers occur when scraping agents

# TODO Check this: https://github.com/AhmedSakrr/Fake-Headers
# TODO User agent integration with scrapy: https://gist.github.com/seagatesoft/e7de4e3878035726731d
# TODO Check how to set referer to previous page when scraping with a followup request (should be in my stackoverflow page)

from user_agent import Generator
from utils      import *
import random as rd


class GenericHeaderGenerator(metaclass = Singleton):

    def __init__(self):

        f = './data/common_agents.txt'
        self.UserAgent  = Generator(by = 'scrape')
        #self.UserAgent  = Generator(by = 'file', filename = f)
        self.Referer    = HTTPHeaderGenerator('./data/referers.json')
        self.Encoder    = AcceptEncoding('./data/acceptEncoding.json')
        self.Language   = AcceptLanguage('./data/languages.json')
        self.Accept     = Accept('./data/accept.json')
        self.compatibilityTable = readJson('./data/header_compatibility.json')
        # NOTE: Version number 0 on the compatibility table means 'header has always been supported'.
        self.domains    = list(self.Referer.data.keys()) # TODO: TypedDict

        return


    def __call__(self) -> dict:

        """ Generates realistic, randomly-chosen HTTP headers.
        Inputs:
            * domain (list) can be either:
                * Empty: random selection among all
                * list containing one or more of: 
                    com, jsp, edu, org, info, net, php3, aspx, biz, uk, it,
                    is,  ua,  cc,  de,  us,   tv,  eu,   ru,   cn,  jp, nl, be,  
                    fr,  ch,  gr,  se,  dk,   bg,  cz,   hu,   lt,  pl, ro, sk, 
                    si,  br,  pt,  es,  il,   au,  io,   no,   ir,  at
            * Browser (list) can be either
                * Empty: random selection among all
                * list containing one or more of: chrome, edge, firefox, safari
            * Device (list) can be either
                * Empty: random selection among all
                * list containing one or more of: mobile/desktop
        """

        # Get a random domain and user agent (TODO: typehints for all)
        domain  = rd.choice(self.domains)
        device  = rd.choice(['mobile', 'desktop'])
        browser = rd.choice(['chrome', 'edge', 'firefox', 'safari'])

        # Generate random applicable user agent
        userAgent = self.UserAgent(browserName = browser, deviceType = device)

        # Get browser version number
        # NOTE: Setting the browser (major) version value to 1 implies that if no version 
        # is found (and returned), all headers will be included in the response on the output 
        # of the removeUnsupported() function.
        version = float(userAgent.browser.get('majorVersion', 1))

        headers = self.makeHeaders(userAgent, domain, browser, version)     # Make all possible headers
        headers = self.removeUnsupported(headers, device, browser, version) # Keep the ones supported by the browser

        # Put headers in correct order
        
        return headers


    def makeHeaders(self, userAgent, domain, browser, version):

        # Make headers dictionary        
        return {
            "User-Agent"                 : userAgent.name,
            "Referer"                    : self.Referer(domain, defaultKey = 'com'), 
            "Accept"                     : self.Accept(browser, version),
            "Accept-Language"            : self.Language(domain),
            "Accept-Encoding"            : self.Encoder(),
            "Sec-CH-UA"                  : userAgent.clientHints['Sec_CH_UA'],
            "Sec-CH-UA-Arch"             : userAgent.clientHints['Sec_CH_UA_Arch'],
            "Sec-CH-UA-Bitness"          : userAgent.clientHints['Sec_CH_UA_Bitness'],
            "Sec-CH-UA-Mobile"           : userAgent.clientHints['Sec_CH_UA_Mobile'],
            "Sec-CH-UA-Model"            : userAgent.clientHints['Sec_CH_UA_Model'],
            "Sec-CH-UA-Platform"         : userAgent.clientHints['Sec_CH_UA_Platform'],
            "Sec-CH-UA-Full-Version-List": userAgent.clientHints['Sec_CH_UA_Full_Version_List'],
            "Sec-CH-UA-Platform-Version" : userAgent.clientHints['Sec_CH_UA_Platform_Version'],
            "Sec-Fetch-Site"             : "same-site",
            "Sec-Fetch-Mode"             : "navigate",
            "Sec-Fetch-User"             : "?1",
            "Sec-Fetch-Dest"             : "document",
            "Upgrade-Insecure-Requests"  : "1"
        }


    def removeUnsupported(self, allHeaders, device, browser, version):
        
        # Get compatible heaers for this browser-device combination
        compatibleHeaders = self.compatibilityTable[f'{browser}-{device}']
        
        headers = {} # Dict to hold only supported headers
        for hName, hValue in allHeaders.items():

            # First version for which <browser> supported the header <headerName>
            minVersion = compatibleHeaders[hName]

            # if header is supported add it to the dict
            if version >= minVersion: headers[hName] = hValue

        return headers


if __name__ == "__main__":
    
    headers = GenericHeaderGenerator()
    
    for _ in range(100):

        h = headers()
        for k, v in h.items():
            pass
        print(h)

