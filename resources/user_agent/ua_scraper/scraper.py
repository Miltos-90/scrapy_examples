""" This module implements the scraper for the user agents from the website http://www.useragentstring.com/.
"""

from bs4                import BeautifulSoup
from random             import choice
from .constants         import AVAILABLE_BROWSERS
from ..ua_parser        import Parser
from ..ua_client_hints  import ClientHintGenerator as CH
from ..templates        import UserAgent
import requests


class Scraper():

    def __init__(self,
        browsers : list = ['Chrome', 'Firefox', 'Safari', 'Edge'], 
        limit    : int  = 20,
        ):
        """ Initialisation method. Scrapes and stores the user agents. 
            Inputs: 
            * browsers: Names of the browsers from which to fetch the user agents
            * limit   : Max number of results (user agents) to fetch for each browser
        """

        # URL to scrape from
        self.baseURL = 'http://www.useragentstring.com/pages/useragentstring.php?name='

        # Check if all browsers are available on the website
        if self.notAvailable(browsers):
            raise ValueError(f'User agent scraper: Non-supported browser detected. Aborting')

        # Generates (scrapes) a list of user agents from the browser list
        self.userAgents = self.getUserAgents(browsers, limit)

        # Instantiate parser object
        self.parser = Parser()
    
        return


    @staticmethod
    def notAvailable(browsers: list):
        """ Checks if all input browsers are available for scraping """
        return bool(set(browsers).difference(AVAILABLE_BROWSERS))


    def getUserAgents(self, browsers : list, limit: int):
        """
        Gathers a list of some active User-Agent strings from 
        http://www.useragentstring.com for the list of browsers
        """

        userAgents = []

        for browser in browsers:
            curAgents = self.getBrowserUserAgents(browser)

            # Limit results if needed
            if limit and len(curAgents) > limit: 
                curAgents = curAgents[:limit]
            
            userAgents.extend(curAgents)

        return userAgents


    def getBrowserUserAgents(self, browser : str) -> list:
        """ Gets the latest User-Agent strings for the given browser """

        url      = self.baseURL + browser
        response = requests.get(url)
        soup     = BeautifulSoup(response.content, 'html.parser')
        uaLinks  = soup.find('div', {'id': 'liste'}).findAll('li')
        uaTexts  = [str(user_agent.a.text) for user_agent in uaLinks]

        return  uaTexts
    

    def __call__(self,
        deviceType  : str = 'desktop', # Device type
        browserName : str = None,      # Browser name
        ) -> UserAgent:
        """ Returns a randomly selected user agent from the given
            device type and browser names
        """

        # Get user agent string
        ua      = UserAgent
        ua.name = choice(self.userAgents)

        # Parse it
        ua.browser, ua.cpu, ua.device, ua.engine, ua.os = self.parser(ua.name) 
        
        # Get User agent hints
        ua.clientHints = CH(ua.browser, ua.cpu, ua.device, ua.os)

        return ua
