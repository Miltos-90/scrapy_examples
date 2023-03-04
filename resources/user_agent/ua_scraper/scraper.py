""" This module implements the scraper for the user agents from the website http://www.useragentstring.com/.
"""

from ..ua_parser        import Parser
from random             import choice
from ..templates        import UserAgent, OS_TYPES
from bs4                import BeautifulSoup
from ..ua_client_hints  import ClientHintGenerator as CH
from collections        import defaultdict
from .                  import constants as c
import requests


class Scraper():

    def __init__(self,
        browsers : list = c.DEFAULT_BROWSERS, 
        limit    : int  = 20,
        ):
        """ Initialisation method. Scrapes and stores the user agents. 
            Inputs: 
            * browsers: Names of the browsers from which to fetch the user agents
            * limit   : Max number of results (user agents) to fetch for each browser
        """

        # Instantiate parser object
        self.parser = Parser()

        # Lowercase inputs
        browsers = [b.lower() for b in browsers]

        # Check if all browsers are available on the website
        if self.notAvailable(browsers):
            raise ValueError(f'User agent scraper: Non-supported browser detected. Aborting')

        # Generate (scrape) a list of user agents from the browser list
        self.userAgents = self.getUserAgents(browsers, limit)

        # Save browser list
        self.browsers = browsers
    
        return

    @staticmethod
    def notAvailable(browsers: list):
        """ Checks if all input browsers are available for scraping """
        return bool(set(browsers).difference(c.AVAILABLE_BROWSERS))


    def getUserAgents(self, browsers : list, limit: int) -> dict:
        """
        Gathers a list of User-Agent strings from 
        http://www.useragentstring.com for the list of browsers
        """

        # Dictionary to hold user agents. It's structure is the following:
        # key: <browser name, device type> (both lowecased), value: user agent string
        agentDict = defaultdict(list)
        
        for browser in browsers:

            # Scrape user agents for this browser
            agents = self.parseURL(browser)

            # Limit results if needed
            if limit and len(agents) > limit: 
                agents = agents[:limit]

            for agent in agents:

                # Extract operating system. If no OS is returned, set to
                # other, which will default to a 'desktop' device type.
                osName  = self.parser.get(agent, ('os', 'name'), 'other')
                osName  = osName.lower().replace(" ", "")

                # Get device type (assume desktop if no device type is returned)
                devType = OS_TYPES.get(osName, 'desktop')
            
                # Add user agent to dictionary
                agentDict[browser.lower(), devType].append(agent)

        return agentDict


    def parseURL(self, browser : str) -> list:
        """ Gets the latest User-Agent strings for the given browser """

        url      = c.BASE_URL + browser
        response = requests.get(url)
        soup     = BeautifulSoup(response.content, 'html.parser')
        links    = soup.find('div', {'id': 'liste'}).findAll('li')
        texts    = [str(link.a.text) for link in links]

        return  texts
    

    def __call__(self,
        browserName : str = None,     # Browser name
        deviceType  : str = 'desktop' # Device type
        ) -> UserAgent:
        """ Returns a randomly selected user agent from the given
            device type and browser names
        """

        ua = UserAgent
        # Choose one at random if not provided
        if not browserName: browserName = choice(self.browsers) 

        # Get a randomly selected user agent string for the selected browser and device type
        applicableAgents = self.userAgents.get( (browserName, deviceType) )

        if applicableAgents:
            ua.name = choice(applicableAgents)

        else:
            # If nothing is found (due to invalid name/type combination), get a chrome/desktop
            # user agent.
            ua.name = choice(self.userAgents.get( ('desktop', 'chrome') ) )

        # Parse user agent string
        ua.browser, ua.cpu, ua.device, ua.engine, ua.os = self.parser(ua.name) 
        
        # Get User agent hints
        ua.clientHints = CH(ua.browser, ua.cpu, ua.device, ua.os)

        return ua
