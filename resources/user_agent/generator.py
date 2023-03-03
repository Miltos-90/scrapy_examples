from .ua_generator import Generator
from dataclasses  import dataclass
from .ua_scraper   import Scraper
from .ua_reader    import Reader
from . import ua_parser as parser
from . import ua_client_hints as ch
import os


@dataclass
class UserAgent():
    """ Class to keep all related data of user agent """
    name        : str
    browser     : parser.Browser
    cpu         : parser.CPU
    device      : parser.Device
    engine      : parser.Engine
    os          : parser.OS
    clientHints : ch.ClientHints


class UserAgentFactory():
    """ User Agent factory """

    def __init__(self, by: str, **kwargs):
        """ 
            User Agent factory: Generates valid user agent strings and associated user client hints.
            * by: Determines generation method. Possible options: 
                - Either generater user agents programmatically (= 'generator'),
                - Scrape them from http://www.useragentstring.com/ (= 'scraper'),
                - Get user agents from a given .txt file (= 'file')
            * kwargs: Corresponding arguments for the generator (see ua_generator/generators.py)
                or the parser (see ua_scraper/scraper.py)
        """

        if   by == 'generator': self.generator = Generator(**kwargs)
        elif by == 'scraper'  : self.generator = Scraper(**kwargs)
        elif by == 'file'     : self.generator = Reader(**kwargs)

        self.parser = parser.Parser()

        return


    @staticmethod
    def _readFile(filename: str) -> list:
        """ Generic txt reader to load user agents. It assumes that 
            each line corresponds to a single user agent string.
        """

        if not os.path.isfile(filename):
            raise FileNotFoundError(f'File {filename} does not exist.')
        
        with open(filename, 'r') as f: x = f.readlines()

        x = [e.strip()for e in x] # Remove leading/trailing spaces

        return x


    def __call__(self) -> UserAgent:
        """ Generate a random user agent """
        
        ua      = UserAgent
        ua.name = self.generator()
        ua.browser, ua.cpu, ua.device, ua.engine, ua.os = self.parser(ua.name) 
        ua.clientHints = ch.ClientHintGenerator(ua.browser, ua.cpu, ua.device, ua.os)

        return ua
