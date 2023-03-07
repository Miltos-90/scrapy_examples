""" This module implements the HeaderGenerator object for a request """


from abc import ABC
from abc import ABCMeta
import json
import random as rd
import os

class Singleton(ABCMeta):
    """ Singleton metaclass """
    _instances = {}

    def __call__(cls, *args, **kwargs):

        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]


class HTTPHeaderGenerator(ABC):
    """ Generic HTTP Header generator class """

    def __init__(self, pathToFile: str):
        """ Initialisation method. Reads necessary data. """
        
        if os.path.isfile(pathToFile):

            with open(pathToFile, mode = 'r', encoding = 'utf-8') as f:
                self.data = json.load(f)

        else:
            raise FileNotFoundError(f"{pathToFile} does not exist.")
        
        return


    def __call__(self, key: str, defaultKey: str) -> str:
        """ Randomly chooses an element from the dictionary <data>
            associated with the attribute <s>. If the attribute does not exist,
            return a randomly selected value from the ones of the <default> key
        """

        exists = key in self.data.keys()
        if exists: return rd.choice(self.data[key])
        else     : return rd.choice(self.data[defaultKey])


    @staticmethod
    def _addqFactors(l:list) -> list:
        """ Appends randomly generated relative quality factors (q-factors) 
            to the elements (strings) of the input list l.
        """
        
        num   = len(l)
        minq  = round(1.0 / num, 1)      # Minimum q value that can be set (maximum = 1.0)
        dq    = (1.0 - minq) / (num + 1) # Reduction rate between cosecutive q values
        qVals = [""]                     # To be populated with the q values
        q     = 1.0                      # Assume first q factor to be equal to 1

        for _ in range(1, num):
            q = rd.uniform(q - dq, q - 2 * dq) # Randomly select a continuously decreasing q factor
            q = max(0.1, round(q, 1))          # round to first decimal and set it to minimum 0.1
            qVals.append(f";q={q}")

        l = [e + q for e, q in zip(l, qVals)] # Append to the elements of the input list

        return l



class AcceptEncoding(HTTPHeaderGenerator):
    """ Generates a random 'Accept-Encoding' header """

    def __init__(self, pathToFile: str):

        super().__init__(pathToFile)

        # The file contains a dict of a single element.
        # Unpack it
        self.data = self.data["Accept-Encoding"]

        return 

    def __call__(self, 
        qIn: bool = None # Indicates if relative quality factors should be included
        ) -> str:
        
        if not qIn: qIn = rd.random() >= 0.5     # Choose if quality factors will be included if not specified
        num      = rd.randint(1, len(self.data)) # Choose a random number <num> of encoding strings to be included
        encoders = rd.sample(self.data, num)     # Make <k> unique random choices from the population of accepted encoders

        if '*' in encoders:     # Always set 'no preference' at the end
            encoders.pop(encoders.index('*')) 
            encoders.append('*')

        if 'gzip' in encoders:  # If 'gzip' is chosen put first  
            encoders.pop(encoders.index('gzip')) 
            encoders.insert(0, 'gzip')

        if qIn:
            encoders = self._addqFactors(encoders)

        return ", ".join(encoders)


class AcceptLanguage(HTTPHeaderGenerator):
    """ Generates a random 'Accept-Language' header """

    
    def __call__(self, 
        domain          : str,                              # Domain to relate languages to
        globalLanguages : list = ['en', 'en-GB', 'en-US'],  # Languages that are always accepted. Set to None to deactivate
        qFactors        : bool = True                       # Indicates if relative quality factors should be included
        ) -> str:

        # Get a language related to the input domain
        domainLanguage = super().__call__(domain, defaultKey = "eu")

        # Prevent the same language from appearing in both the domain-specific language and the universal languages
        dupe = domainLanguage in globalLanguages
        if not dupe : languages = [domainLanguage] + globalLanguages
        else        : languages = globalLanguages

        # Add relative quality factors
        if qFactors: languages = self._addqFactors(languages)

        return ",".join(languages)




# Headers to do
def fetchDest() -> str:
    """ Generates the value of the Sec-Fetch-Dest header.
        See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-Fetch-Dest
    """ 
    # TODO
    return

def fetchMode() -> str:
    """ Generates the value of the Sec-Fetch-Mode header.
        See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-Fetch-Mode
    """ 
    # TODO
    return

def fetchSite() -> str:
    """ Generates the value of the Sec-Fetch-Site header.
        See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-Fetch-Site
    """ 
    # TODO
    return

def fetchUser() -> str:
    """ Generates the value of the Sec-Fetch-User header.
        See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-Fetch-User
    """ 
    # TODO
    return

def upgradeRequests() -> str:
    """ Generates the value of the Upgrade-Insecure-Requests header.
        See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Upgrade-Insecure-Requests
    """ 
    # TODO
    return
