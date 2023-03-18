""" Implements a factory for objects that generate user agents (Programmer, Scraper, Reader) """

from .ua_programmer import Programmer
from .extractors    import Scraper, Reader
from typing         import Union


def factory(by: str, **kwargs) -> Union[Programmer, Scraper, Reader]:
    """
        User Agent factory: Generates user agent strings and associated user client hints.
        * by: Determines generation method. Possible options: 
            - Either generater user agents programmatically     (= 'programmer'),
            - Scrape them from http://www.useragentstring.com/  (= 'scraper'),
            - Get user agents from a given .txt file            (= 'file')
        * kwargs: Corresponding arguments for each generator
    """

    if   by == 'program': return Programmer(**kwargs)
    elif by == 'scrape' : return Scraper(**kwargs)
    elif by == 'file'   : return Reader(**kwargs)
    else: raise ValueError(f"User agent generation method {by} not implemented.")
