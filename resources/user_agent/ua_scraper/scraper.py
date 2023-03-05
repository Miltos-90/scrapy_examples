""" This module implements the scraper for the user agents from the website http://www.useragentstring.com/.
"""

from ..definitions  import OS_TYPES
from ..template     import BaseGenerator
from bs4            import BeautifulSoup
from collections    import defaultdict
from .              import constants as c
import requests


class Scraper(BaseGenerator):
    """ Generates user agent strings scraped from http://www.useragentstring.com/"""

    def __init__(self,
        browsers : list[str] = c.DEFAULT_BROWSERS, 
        limit    : int       = 20,
        ):
        """ Initialisation method. Scrapes and stores the user agents. 
            Inputs: 
            * browsers: Names of the browsers from which to fetch the user agents
            * limit   : Max number of results (user agents) to fetch for each browser
        """

        super().__init__()

        self.browsers = [b.lower() for b in browsers] # Lowercase inputs

        # Check if all browsers are available on the website
        if self._browsersNotAvailable():
            raise ValueError(f'User agent scraper: Non-supported browser detected. Aborting')

        # Generate (scrape) a dict of user agents from the browser list. It's structure is:
        # key: <browser name, device type> (both lowecased), value: user agent string
        self.userAgents = self._getUserAgents(limit)

        return


    def _browsersNotAvailable(self) -> bool:
        """ Checks if all input browsers are available for scraping """
        return bool(set(self.browsers).difference(c.AVAILABLE_BROWSERS))


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
                osName  = osName.lower().replace(" ", "")

                # Get device type (assume desktop if no device type is returned)
                devType = OS_TYPES.get(osName, 'desktop')
            
                # Add user agent to dictionary
                agentDict[browser, devType].append(agent)

        return agentDict


    def _parseURL(self, browser : str) -> list:
        """ Gets the latest User-Agent strings for the given browser """

        url      = c.BASE_URL.format(name = browser)
        response = requests.get(url)
        soup     = BeautifulSoup(response.content, 'html.parser')
        texts    = [link.a.text for link in soup.findAll('li')]
        
        return  texts