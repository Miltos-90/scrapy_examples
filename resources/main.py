""" HTTP header generator. 
    Partially based on the repo: https://github.com/MichaelTatarski/fake-http-header

"""
# TODO: Replace get_args(DEVICE_TYPE) BROWSER TYPE etc with constants.
# TODO: Line 269.

# TODO Check this when writing package: https://github.com/AhmedSakrr/Fake-Headers
# Tips and tricks: https://scrapeops.io/web-scraping-playbook/web-scraping-guide-header-user-agents/#ensuring-proper-header-order

from client_hints     import ClientHintGenerator
from typing           import Union, Any, Dict
from collections      import OrderedDict
from typing           import get_args
from ua_generator     import Generator
from ua_parser        import Parser
import definitions    as defs
import helper_classes as hc
import utils
import warnings


class HeaderGenerator(metaclass = utils.Singleton):

    def __init__(self, by: defs.GENERATOR_TYPE = 'program', **kwargs):

        self.UserAgent   = Generator(by = by, **kwargs)
        self.Parser      = Parser()
        self.ClientHints = ClientHintGenerator()
        self.Referer     = hc.HTTPHeaderGenerator('./data/referers.json')
        self.Encoder     = hc.AcceptEncoding('./data/acceptEncoding.json')
        self.Language    = hc.AcceptLanguage('./data/languages.json')
        self.Accept      = hc.Accept('./data/accept.json')
        self.Selector    = utils.Selector()
        self.domains     = list(self.Referer.data.keys())

        self.devices     = get_args(defs.DEVICE_TYPE)  # Available devices
        self.browsers    = get_args(defs.BROWSER_TYPE) # Available browsers

        # Header names compatible with each browser-version combination
        self.compTable   = utils.readFile('./data/header_compatibility.json')

        # Order of the headers for each browser
        self.headerOrder = utils.readFile('./data/header_order.json')

        return


    def _checkInput(self, 
        inputType: defs.INPUT_TYPE,  # Type of input to check or return
        value    : Union[None, str], # Corresponding value provided by the user
        **kwargs) -> Any:
        """ Checks user input if provided, otherwise it returns realistic randomly 
            selected values according to usage/market statistics data.
        """

        if not value: 
            # User did not supply a value for the input. Produce one.
            return self.Selector(inputType, **kwargs)

        else:         
            # Check if user input is valid.
            value  = value.lower()

            if   inputType not in ["browser", "device", "domain"]:      errMsg = "Invalid input type."
            elif inputType == "browser" and value not in self.browsers: errMsg = "Invalid browser name."
            elif inputType == "device"  and value not in self.devices:  errMsg = "Invalid device type."
            elif inputType == "domain"  and value not in self.domains:  errMsg = "Invalid domain."
            else:                                                       errMsg = None

            if errMsg: raise ValueError(errMsg)
            else     : return value


    @staticmethod
    def _warnOnOverwrite(
        inputType : defs.INPUT_TYPE,    # Type of input being checked (used to print warning)
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


    @staticmethod
    def _makeCookieHeader(cookieDict: Dict[str, str]) -> str:
        """ Generates the <Cookie> header given a dict of cookies """

        # Convert dictionary of cookies to a list of {'name': <name>, 'value': <value>} dicts
        cookieList = [{'name': key, 'value': value} for key, value in cookieDict.items()]
        
        # Convert to string
        # Format first cookie
        cookie    = cookieList.pop()
        cookieStr = f"{cookie['name']}={cookie['value']}"

        # Format subsequent cookies
        for c in cookieList: cookieStr += f"; {c['name']}={c['value']}"

        return cookieStr


    def _makeHeaders(self, 
        userAgent: str,                 # user agent
        browser  : defs.BROWSER_TYPE,   # browser name
        device   : defs.DEVICE_TYPE,    # device type
        domain   : defs.DOMAIN_TYPE,    # domain name
        cookies  : Dict[str, str] = {}  # Cookies dictionary
        ) -> dict:
        """ Generates headers dictionary, given a user agent string,
            a browser name, and a top-level domain.
        """

        # Extract required info from the user agent
        brVersion = self.Parser.get(userAgent, ('browser', 'majorVersion'))
        brVersion = float(brVersion) # str -> int
        
        # Make (partial) header dictionary
        allHeaders: dict[str, str] =  {
            "User-Agent"      : userAgent,
            "Referer"         : self.Referer(domain, defaultKey = 'com'), 
            "Accept"          : self.Accept(browser, brVersion),
            "Accept-Language" : self.Language(domain),
            "Accept-Encoding" : self.Encoder(),
        }

        # Add client hints
        ch = self.ClientHints(userAgent)         
        allHeaders.update(ch)

        # Add cookies
        if bool(cookies):                       # 
            allHeaders['Cookie'] = self._makeCookieHeader(cookies)

        # Add constant-valued headers
        allHeaders.update(defs.CONSTANT_HEADERS)

        # return compatible headers only
        return self._getCompatibleHeaders(allHeaders, browser, device, brVersion)

    
    def _getCompatibleHeaders(self, 
        allHeaders: dict,               # Dict with all the headers
        browser   : defs.BROWSER_TYPE,  # browser name
        device    : defs.DEVICE_TYPE,   # device type
        browserVersion: float,          # browser version
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
    def _makeVersionCompatible(httpVersion: defs.HTTP_VERSION_TYPE, headers: dict) -> dict:
        """ Makes header dict compatible to HTTP version 2.0, i.e.
            it lowercases their names.
         """

        if httpVersion == 2:
            headers = {k.lower(): v for k, v in headers.items()}
        
        return headers


    def _orderHeaders(self, 
        httpVersion : defs.HTTP_VERSION_TYPE, 
        browser     : defs.BROWSER_TYPE,
        headers     : Dict[str, str]
        ) -> OrderedDict:
        """ Converts the headers dictionary to an ordered dict based on the browser
            and http versions.
         """

        # Extract order for current http version and browser
        if httpVersion == 1: 
            orderedHeaderNames = self.headerOrder["http version 1.x"][browser]
        else: 
            orderedHeaderNames = self.headerOrder["http version 2.x"][browser]

        # Make ordered dictionary
        headersOrdered = OrderedDict()
        for hName in orderedHeaderNames:
            if hName in headers: # header might not exist for older versions
                headersOrdered[hName] = headers.pop(hName)
        
        # Add the remaining headers (in an unordered manner)
        for hName, hValue in headers.items():
            headersOrdered[hName] = hValue
        
        return headersOrdered
    

    def __call__(self,
        domain      : Union[None, defs.DOMAIN_TYPE]  = None, 
        device      : Union[None, defs.DEVICE_TYPE]  = None, 
        browser     : Union[None, defs.BROWSER_TYPE] = None,
        httpVersion : defs.HTTP_VERSION_TYPE = 1,
        cookies     : Dict[str, str] = {},
        ) -> OrderedDict:

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
            * Cookies: Dictionary of <name>, <value> pairs containing cookies 
        """

        # Validate user supplied values
        browser_ = self._checkInput(inputType = 'browser', value = browser)
        device_  = self._checkInput(inputType = 'device',  value = device)
        domain_  = self._checkInput(inputType = 'domain',  value = domain)
        if httpVersion not in get_args(defs.HTTP_VERSION_TYPE): 
            raise ValueError('Invalid http version.')

        # Generate random applicable user agent and client hints
        # NOTE: User-supplied values may be overwriten in the search for a valid user agent.
        browser_, device_, userAgent = self.UserAgent(browser_, device_)
        
        userAgent = 'SAMSUNG-GT-i8000/1.0 (Windows CE; Opera Mobi; U; en) Opera 9.5'
        #UserAgent = 'Opera/12.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.02'
        try:
            # Make header dict (This function will fail in case a user agent cannot be parsed.
            # This can happen when a 'bad' user agent string is imported from the filename 
            # provided by the user)
            headers = self._makeHeaders(userAgent, browser_, device_, domain_, cookies)

        except:

            # Warn for occured exception
            warnings.warn(f'Failed to generate headers for agent: {userAgent}. Retrying with another agent.')
            
            # Blacklist this user agent
            self.UserAgent.remove(userAgent) 

            # Try generating headers by choosing another user agent
            browser_, device_, userAgent = self.UserAgent(browser_, device_)
            headers = self._makeHeaders(userAgent, browser_, device_, domain_, cookies)

            # TODO: What if dict gets empty?

        # Ensure http version compatibility (i.e. lowercase if needed)
        headers = self._makeVersionCompatible(httpVersion, headers)

        # Put headers in the correct order
        headers = self._orderHeaders(httpVersion, browser_, headers)

        # Print a warning if input values were overwritten
        self._warnOnOverwrite(inputType = 'browser', userValue = browser, newValue = browser_)
        self._warnOnOverwrite(inputType = 'device',  userValue = device, newValue = device_)

        return headers

    
if __name__ == "__main__":

    
    cookies = {'sp_landing': 'https%3A%2F%2Fopen.spotify.com%2Fcollection%2Fplaylists%3Fsp_cid%3De8417a6b1784a200a50c049666bed54a%26device%3Ddesktop', 'sp_t': 'e8417a6b1784a200a50c049666bed54a'}
    
    #f = './common_agents.txt'
    #f = './agents_for_testing.txt'
    
    #headers = HeaderGenerator(by = 'file', filename = f)
    headers = HeaderGenerator(by = 'scrape')
    e = 0
    for _ in range(1):
        h = headers(httpVersion=1, cookies=cookies)
        
        for k, v in h.items():
            print(k, v)
        
        if not bool(h): e+= 1
    #print()
    print(e)
