""" Implements a factory for user agent generator objects. """

from .ua_programmer   import Programmer
from .ua_scraper      import Scraper
from .ua_reader       import Reader


def UserAgentGeneratorFactory(by: str, **kwargs):
    """
        User Agent factory: Generates user agent strings and associated user client hints.
        * by: Determines generation method. Possible options: 
            - Either generater user agents programmatically (= 'generator'),
            - Scrape them from http://www.useragentstring.com/ (= 'scraper'),
            - Get user agents from a given .txt file (= 'file')
        * kwargs: Corresponding arguments for the generator (see generator.py)
            or the parser (see ua_scraper/scraper.py)
    """

    if   by == 'program' : return Programmer(**kwargs)
    elif by == 'scrape'  : return Scraper(**kwargs)
    elif by == 'file'    : return Reader(**kwargs)
    else: raise ValueError(f" User agent generation method {by} not implemented.")
