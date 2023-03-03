from ua_client_hints import ClientHints
from ua_generator import Generator
from ua_scraper import Scraper
from ua_parser import Parser
from random import choice
from abc import ABCMeta
import os


class Singleton(ABCMeta):
    """ Singleton metaclass """
    _instances = {}

    def __call__(cls, *args, **kwargs):

        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]


class UserAgent(metaclass = Singleton):
    """ User Agent factory """

    def __init__(self, by: str, **kwargs):
        """ 
            * by: Determines generation method. Possible options: 
                - Either generater user agents programmatically (= 'generator'),
                - Scrape them from http://www.useragentstring.com/ (= 'scraper'),
                - Get user agents from a given .txt file (= 'file')
            * kwargs: Corresponding arguments for the generator (see ua_generator/generators.py)
                or the parser (see ua_scraper/scraper.py)
        """

        # Instantiate generator method or object
        if by == 'generator':
            self.generator = Generator(**kwargs)

        elif by == 'scraper':
            self.generator = Scraper(**kwargs)
        
        elif by == 'file':
            agents         = self._readFile(kwargs.get('filename'))
            self.generator = lambda: choice(agents) # Randomly select an agent from the file

        # Instantiate parser
        self.parser = Parser()

        return


    @staticmethod
    def _readFile(filename: str) -> list:
        """ Generic txt reader to load user agents. It assumes that 
            each line corresponds to a single user agent string.
        """

        if not os.path.isfile(filename):
            raise FileNotFoundError(f'File {filename} does not exist.')
        
        with open(filename, 'r') as f:
            x = f.readlines()     # read into a list
        x = [e.strip()for e in x] # Remove leading/trailing spaces

        return x


    def __call__(self):

        ua = self.generator() # Get a user agent
        d  = self.parser(ua)  # Parse it
        ch = ClientHints(d)   # Generate client hints

        return ua, ch
