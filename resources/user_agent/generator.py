from .ua_programmer   import Programmer
from .ua_scraper      import Scraper
from .ua_reader       import Reader
from .templates       import UserAgent

class UserAgentGenerator():
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

        if   by == 'program' : self.generator = Programmer(**kwargs)
        elif by == 'scrape'  : self.generator = Scraper(**kwargs)
        elif by == 'file'    : self.generator = Reader(**kwargs)

        return


    def __call__(self,
        browserName: str = None,      # Browser name
        deviceType : str = 'desktop', # Device type
        ) -> UserAgent:
        """ Generate a random user agent """
        
        # Get user agent string
        return self.generator(browserName = browserName, deviceType = deviceType)
        


