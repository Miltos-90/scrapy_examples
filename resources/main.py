""" HTTP header generator. 
    Partially based on the repo: https://github.com/MichaelTatarski/fake-http-header

"""
# TODO Fix header order (and fix source on the md file) (make orderedDict in collections)
# TODO: Some headers are empty (only from scraping)

# TODO Check this when writing package: https://github.com/AhmedSakrr/Fake-Headers
# Tips and tricks: https://scrapeops.io/web-scraping-playbook/web-scraping-guide-header-user-agents/#ensuring-proper-header-order

from typing       import get_args
from ua_generator import Generator
from ua_parser    import Parser
from client_hints import ClientHintGenerator
from typing       import Union, Any, Literal
from definitions  import BROWSER_TYPE, DEVICE_TYPE, INPUT_TYPE, DOMAIN_TYPE
from helpers      import HTTPHeaderGenerator, AcceptEncoding, AcceptLanguage, Accept
from utils        import Selector, Singleton, readFile
import warnings



class HeaderGenerator(metaclass = Singleton):

    def __init__(self):

        f = './data/common_agents.txt'
        f = './agents_for_testing.txt'
        self.UserAgent   = Generator(by = 'scrape')
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

        return


    def _checkInput(self, 
        inputType: INPUT_TYPE,       # Type of input to check or return
        value    : Union[None, str], # Corresponding value provided by the user
        **kwargs) -> Any:
        """ Checks user input if provided, otherwise it returns realistic randomly 
            selected values according to usage/market statistics data.
        """

        if not value: # User did not supply a value for the input. Produce one.
            return self.Selector(inputType, **kwargs)

        else:         # Check if user input is valid.
            value  = value.lower()
            errMsg = None

            if   inputType == 'browser' and value not in self.browsers: errMsg = 'Invalid browser name.'
            elif inputType == 'device'  and value not in self.devices:  errMsg = 'Invalid device type.'
            elif inputType == 'domain'  and value not in self.domains:  errMsg = 'Invalid domain.'
            else: errMsg = "Invalid input type."

            if errMsg: raise ValueError(errMsg)
            else     : return value


    @staticmethod
    def _warnOnOverwrite(
        inputType : INPUT_TYPE,         # Type of input being checked (used to print warning)
        userValue : Union[None, str],   # Input value supplied by the user
        newValue  : str                 # Value used for the generation of the user agent
        ):
        """ Compares the values of the user inputs, and the values used for the genration of the user agent.
            If they do not match, a warning is printed.
        """

        if userValue and newValue != userValue.lower():
            msg = f'{inputType.title()} overwritten to find suitable user agent.'
            warnings.warn(message = msg)

        return


    def _makeHeaders(self, 
        userAgent: str,            # user agent
        browser  : BROWSER_TYPE,   # browser name
        device   : DEVICE_TYPE,    # device type
        domain   : DOMAIN_TYPE     # domain name
        ) -> dict:
        """ Generates headers dictionary, given a user agent string,
            a browser name, and a top-level domain.
         """

        # Extract required info from the user agent
        brVersion = self.Parser.get(userAgent, ('browser', 'majorVersion'))
        brVersion = float(brVersion) # str -> int

        # Make header dictionary
        allHeaders: dict[str, str] =  {
            "User-Agent"                : userAgent,
            "Referer"                   : self.Referer(domain, defaultKey = 'com'), 
            "Accept"                    : self.Accept(browser, brVersion),
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

        # return compatible headers only
        return self._getCompatibleHeaders(allHeaders, browser, device, brVersion)

    
    def _getCompatibleHeaders(self, 
        allHeaders: dict,           # Dict with all the headers
        browser   : BROWSER_TYPE,   # browser name
        device    : DEVICE_TYPE,    # device type
        browserVersion: float,      # browser version
        ) -> dict:
        """ Extracts compatible headers for a given browser (and version) and device"""

        # Get compatible header names (keys) and versions (values)
        compatibleTab = self.compTable[f'{browser}-{device}']
        
        headers = {} # Dict that contains the compatible headers only
        for hName, hValue in allHeaders.items():

            # 1st version for which <browser> supported <hName>
            minVersion  = compatibleTab[hName]

            # if header <hName> is supported for the given version, add it to the dict
            if browserVersion >= minVersion: headers[hName] = hValue 

        return headers

    
    @staticmethod
    def _makeVersionCompatible(httpVersion: int, headers: dict) -> dict:
        """ Makes header dict compatible to HTTP version 2.0, i.e.
            it lowercases their names.
         """

        if httpVersion == 2:
            headers = {k.lower(): v for k, v in headers.items()}
        
        return headers


    def __call__(self,
        domain : Union[None, DOMAIN_TYPE] = None, 
        device : Union[None, DEVICE_TYPE] = None, 
        browser: Union[None, DEVICE_TYPE] = None,
        httpVersion: Literal[1, 2] = 1,
        ) -> dict:

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
            * HTTP version (int), can be either 1 (supports both 1.0 and 1.1) or 2 (2.0)
        """

        # Validate user supplied values
        browser_ = self._checkInput(inputType = 'browser', value = browser)
        device_  = self._checkInput(inputType = 'device',  value = device)
        domain_  = self._checkInput(inputType = 'domain',  value = domain)
        if httpVersion not in [1, 2]: raise ValueError('Invalid http version.')

        # Generate random applicable user agent and client hints
        # NOTE: User-supplied values may be overwriten in the search for a valid user agent.
        browser_, device_, userAgent = self.UserAgent(browser_, device_)

        # Print a warning if input values are overwritten
        self._warnOnOverwrite(inputType = 'browser', userValue = browser, newValue = browser_)
        self._warnOnOverwrite(inputType = 'device',  userValue = device, newValue = device_)
        
        # Make header dict
        headers = self._makeHeaders(userAgent, browser_, device_, domain_)

        # Make compatible to the given http version
        headers = self._makeVersionCompatible(httpVersion, headers)

        # Put in the correct order
        
        return headers

    
if __name__ == "__main__":
    
    
    headers = HeaderGenerator()
    
    e = 0
    for _ in range(1000):

        h = headers(httpVersion=2)
        
        #print(h)
        if not bool(h): 
            e+= 1

    print(e)
