""" This module implements the scraper for the user agents from the website http://www.useragentstring.com/.
"""

from bs4 import BeautifulSoup
from random import choice
import requests
from ua_scraper.constants import AVAILABLE_BROWSERS

class Scraper():

    def __init__(self,
        browsers : list = ['Chrome', 'Firefox', 'Mozilla', 'Safari', 'Opera', 'Edge'], 
        limit    : int  = 20,
        ):
        """ Initialisation method. Scrapes and stores the user agents. 
            Inputs: 
            * browsers: Names of the browsers from which to fetch the user agents
            * limit   : Max number of results (user agents) to fetch for each browser
        """

        # URL to scrape from
        self.baseURL = 'http://www.useragentstring.com/pages/useragentstring.php?name='

        # Input check
        if bool(set(browsers).difference(AVAILABLE_BROWSERS)):
            raise ValueError(f'User agent scraper: Non-supported browser detected. Aborting')


        # Generates (scrapes) a list of user agents from the browser list
        self.userAgents = self.getUserAgents(browsers, limit)
    
        return


    def getUserAgents(self, browsers : list, limit: int):
        """
        Gathers a list of some active User-Agent strings from 
        http://www.useragentstring.com for the list of browsers
        """

        userAgents = []

        for browser in browsers:
            curAgents = self.getBrowserUserAgents(browser)

            # Limit results if needed
            if limit is not None and len(curAgents) > limit: 
                curAgents = curAgents[:limit]
            
            userAgents.extend(curAgents)

        with open('./agents.txt', 'a') as f:
            for line in userAgents:
                f.write(f"{line}\n")

        return userAgents


    def getBrowserUserAgents(self, browser : str) -> list:
        """ Gets the latest User-Agent strings for the given browser """

        url      = self.baseURL + browser
        response = requests.get(url)
        soup     = BeautifulSoup(response.content, 'html.parser')
        uaLinks  = soup.find('div', {'id': 'liste'}).findAll('li')
        uaTexts  = [str(user_agent.a.text) for user_agent in uaLinks]

        return  uaTexts
    

    def __call__(self):
        """ Returns a randomly selected user agent """
        return choice(self.userAgents)
