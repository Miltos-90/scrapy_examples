from ua_parser import Parser
from ua_generator import Generator
from ua_scraper import Scraper
from ua_client_hints import ClientHints
import os
from random import choice
from abc import ABCMeta


class Singleton(ABCMeta):
    """ Singleton metaclass """
    _instances = {}

    def __call__(cls, *args, **kwargs):

        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]


class UserAgentGenerator(metaclass = Singleton):
    """ User Agent factory """

    def __init__(self, how: str, **kwargs):
        """ 
            * how: Determines generation method. Possible options: 
                - Either generater user agents programmatically (= 'generate'),
                - Scrape them from http://www.useragentstring.com/ (= 'scrape'),
                - Get user agents from a given .txt file (= 'file')
            * kwargs: Corresponding arguments for each object
        """

        # Instantiate generator method or object
        if how == 'generate':
            self.generator = Generator(**kwargs)

        elif how == 'scrape':
            self.generator = Scraper(**kwargs)
        
        elif how == 'file':
            agents = self._readFile(kwargs.get('filename'))
            self.generator = lambda: choice(agents)

        # Instantiate parser
        #self.parser = Parser(**kwargs)

        return


    @staticmethod
    def _readFile(filename: str) -> list:
        """ Generic txt reader. """

        if not os.path.isfile(filename):
            raise FileNotFoundError(f'File {filename} does not exist.')
        
        with open(filename, 'r') as f:
            x = f.readlines()       # read into a list
        x = [e.strip()for e in x]   # Remove leading/trailing spaces

        return x


    def __call__(self):

        # Get a user agent (either generated programmatically or parsed)
        userAgent = self.generator()

        # Parse it
        #d = self.parser(userAgent)

        # Generate client hints
        #ch = ClientHints(d)

        return userAgent, None



if __name__ == '__main__':
    
    g = UserAgentGenerator(how = 'file', filename = 'user_agents.txt')

    for _ in range(10):
        ua, ch = g()
        print(ua)