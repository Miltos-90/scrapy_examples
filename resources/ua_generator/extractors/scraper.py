""" This module implements the scraper for the user agents from the website http://www.useragentstring.com/.
"""

from definitions   import BROWSER_TYPE
from .extractor    import Extractor
from bs4           import BeautifulSoup
from utils         import readFile
from typing        import List, get_args
import requests

BASE_URL = 'http://www.useragentstring.com/pages/useragentstring.php?name={name}' # URL from which to scrape from


class Scraper(Extractor):
    """ Generates user agent strings scraped from http://www.useragentstring.com/"""

    def __init__(self,
        browsers : tuple = get_args(BROWSER_TYPE),
        limit    : int   = 20,
        ):
        """ Initialisation method. Scrapes and stores the user agents. 
            Inputs: 
            * browsers: Names of the browsers from which to fetch the user agents
            * limit   : Max number of results (user agents) to fetch for each browser.
                        Note that they are order from most recent to older ones
        """
        
        super().__init__()

        browsers_: List[BROWSER_TYPE] = [b.lower() for b in browsers]
        self._isAvailable(browsers_)
        self._get(browsers_, limit)

        return


    def _isAvailable(self, browsers: List[BROWSER_TYPE]):
        """ Checks if all input browsers are available for scraping. Raises error if not """

        # Get available browsers
        lines       = readFile('./data/scraper_browsers.txt')
        allBrowsers = set( [b.rstrip('\n') for b in lines] )

        if bool(set(browsers).difference(allBrowsers)):
            raise ValueError(f'User agent scraper: Non-supported browser detected. Aborting')
        
        return


    def _get(self, browsers: List[BROWSER_TYPE], limit: int):
        """
        Gathers a list of User-Agent strings from 
        http://www.useragentstring.com for the list of browsers
        """
        
        for browser in browsers:
            agents = self._scrape(browser, limit)
            [self._add(agent) for agent in agents]
        
        self._check()

        return


    def _scrape(self, browser : str, limit: int) -> list:
        """ Scrapes the latest User-Agent strings for the given browser """

        url      = BASE_URL.format(name = browser)
        response = requests.get(url)
        soup     = BeautifulSoup(response.content, 'html.parser')
        texts    = [link.a.text for link in soup.findAll('li')]

        # Limit scraped results if needed
        if limit and len(texts) > limit: texts = texts[:limit]

        return  texts