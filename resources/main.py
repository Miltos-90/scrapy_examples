""" HTTP header generator. 
    Partially based on the repo: https://github.com/MichaelTatarski/fake-http-header

"""
# TODO Fix header order (and fix source on the md file)
# TODO: Fix typehints on main
# TODO: Some headers are empty (not from common agents.txt or when programming)

# TODO Check this: https://github.com/AhmedSakrr/Fake-Headers
# TODO User agent integration with scrapy: https://gist.github.com/seagatesoft/e7de4e3878035726731d
# TODO Check how to set referer to previous page when scraping with a followup request (should be in my stackoverflow page)


from typing import get_args
from ua_generator import Generator
from ua_parser import Parser
from client_hints import ClientHintGenerator
from definitions import BROWSER_TYPE, DEVICE_TYPE
from utils      import *
import random as rd


class GenericHeaderGenerator(metaclass = Singleton):

    def __init__(self):

        f = './data/common_agents.txt'
        f = './agents_for_testing.txt'
        self.UserAgent   = Generator(by = 'program')
        #self.UserAgent   = Generator(by = 'file', filename = f)
        self.Parser      = Parser()
        self.ClientHints = ClientHintGenerator()
        self.Referer     = HTTPHeaderGenerator('./data/referers.json')
        self.Encoder     = AcceptEncoding('./data/acceptEncoding.json')
        self.Language    = AcceptLanguage('./data/languages.json')
        self.Accept      = Accept('./data/accept.json')
        self.Selector    = Selector()
        self.domains     = list(self.Referer.data.keys())
        self.devices     = get_args(DEVICE_TYPE)
        self.browsers    = get_args(BROWSER_TYPE)
        self.compTable   = readFile('./data/header_compatibility.json')
        # NOTE: Version number 0 on the compatibility table <compTable> 
        # means 'header has always been supported'.

        return


    def __call__(self, domain = None, device = None, browser = None) -> dict:

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

        # Check or select inputs if needed        
        if not device:
            device = self.Selector.device()
        else:
            device = device.lower()
            if device not in self.devices: raise ValueError(f'Invalid device type')

        if not browser: 
            browser = self.Selector.browser(device) 
        else:
            browser = browser.lower()
            if browser not in self.browsers: 
                raise ValueError(f'Invalid browser name')

        domain  = rd.choice(self.domains) if not domain else domain

        # Generate random applicable user agent and client hints
        # NOTE: This function may overwrite the user-supplied 
        #       values if an applicable user agent is not found.
        browser, device, userAgent = self.UserAgent(browser, device)
        
        # Extract required info from the user agent
        version = self.Parser.get(userAgent, ('browser', 'majorVersion'))
        version = float(version) # str -> int

        # Make header dictionary (includes all headers)      
        allHeaders =  {
            "User-Agent"                : userAgent,
            "Referer"                   : self.Referer(domain, defaultKey = 'com'), 
            "Accept"                    : self.Accept(browser, version),
            "Accept-Language"           : self.Language(domain),
            "Accept-Encoding"           : self.Encoder(),
            "Sec-Fetch-Site"            : "same-site",
            "Sec-Fetch-Mode"            : "navigate",
            "Sec-Fetch-User"            : "?1",
            "Sec-Fetch-Dest"            : "document",
            "Upgrade-Insecure-Requests" : "1"
        }

        # Add client hints
        ch = self.ClientHints(userAgent)
        allHeaders.update(ch)

        print(userAgent)
        
        
        # Get compatible header names for this browser-device combination
        compatibleHeaders = self.compTable[f'{browser}-{device}']
        
        # Keep only the compatible headers
        headers = {}
        for hName, hValue in allHeaders.items():

            minVersion  = compatibleHeaders[hName]            # 1st version for which <browser> supported <hName>
            if version >= minVersion: headers[hName] = hValue # if <hName> is supported, add it to the dict

        # Put headers in correct order

        #if not bool(headers):
        #    print(device, browser, version, userAgent.name)
            
        
        return headers


    
if __name__ == "__main__":
    
    headers = GenericHeaderGenerator()
    
    e = 0
    for _ in range(1000):

        h = headers()
        #for k, v in h.items():
        #    pass
        #pass
        #print(h)
        if not bool(h): 
            e+= 1

        break

    #print(e)

