""" This module implements the scraper for the user agents from the website http://www.useragentstring.com/.
"""

from .generator    import BaseGenerator
from bs4           import BeautifulSoup
from collections   import defaultdict
import requests

# URL from which to scrape from
BASE_URL = 'http://www.useragentstring.com/pages/useragentstring.php?name={name}'


class Scraper(BaseGenerator):
    """ Generates user agent strings scraped from http://www.useragentstring.com/"""

    def __init__(self,
        browsers : list[str] = ['chrome', 'firefox', 'safari', 'edge'],
        limit    : int       = 20,
        ):
        """ Initialisation method. Scrapes and stores the user agents. 
            Inputs: 
            * browsers: Names of the browsers from which to fetch the user agents
            * limit   : Max number of results (user agents) to fetch for each browser
        """
        
        super().__init__()

        # Read available browser list
        with open('./data/scraper_browsers.txt', 'r') as f: 
            lines = f.readlines()

        availableBrowsers = set( [b.rstrip('\n') for b in lines] )
        
        # Lowercase inputs
        browsers = [b.lower() for b in browsers]

        # Check if all user-supplied browsers are available on the website
        if self._NotAvailable(browsers, availableBrowsers):
            raise ValueError(f'User agent scraper: Non-supported browser detected. Aborting')

        else:
            self.browsers = browsers

        # Generate (scrape) a dict of user agents from the browser list. It's structure is:
        # key: <browser name, device type> (both lowecased), value: user agent string
        self.userAgents = self._getUserAgents(limit)

        return


    @staticmethod
    def _NotAvailable(browsers, allBrowsers) -> bool:
        """ Checks if all input browsers are available for scraping """
        return bool(set(browsers).difference(allBrowsers))


    def _getUserAgents(self, limit: int) -> dict[str, list]:
        """
        Gathers a list of User-Agent strings from 
        http://www.useragentstring.com for the list of browsers
        """

        # Dictionary to hold user agents. It's structure is the following:
        # key: <browser name, device type> (both lowecased), value: user agent string
        agentDict = defaultdict(list)
        
        for browser in self.browsers:

            # Scrape user agents for this browser
            agents = self._parseURL(browser)

            # Limit results if needed
            if limit and len(agents) > limit: 
                agents = agents[:limit]

            for agent in agents:

                # Extract operating system. If no OS is returned, set to
                # other, which will default to a 'desktop' device type.
                osName  = self.parser.get(agent, ('os', 'name'), 'other')
                osName  = osName.lower()

                # Get device type (assume desktop if no device type is returned)
                devType = self.osTypes.get(osName, 'desktop')
            
                # Add user agent to dictionary
                agentDict[browser, devType].append(agent)

        return agentDict


    def _parseURL(self, browser : str) -> list:
        """ Gets the latest User-Agent strings for the given browser """

        url      = BASE_URL.format(name = browser)
        response = requests.get(url)
        soup     = BeautifulSoup(response.content, 'html.parser')
        texts    = [link.a.text for link in soup.findAll('li')]
        
        return  texts