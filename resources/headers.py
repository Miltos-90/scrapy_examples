import json
import random as rd
import re
from abc import ABC
import os


def RelativeQualityFactorGenerator(num) -> list:
    """ Returns a list of <num> randomly chosen relative quality factors """

    minq  = round(1 / num, 1)       # Minimum q value that can be set (maximum = 1.0)
    dq    = (1.0-minq) / (num + 1)  # Reduction rate between cosecutive q values
    qVals = [""]                    # To be populated with the q values
    q     = 1.0                     # Assume first q factor to be equal to 1

    for _ in range(1, num):
        q = rd.uniform(q - dq, q - 2 * dq)
        q = max(0.1, round(q, 1))
        qVals.append(f";q={q}")

    return qVals

class HTTPHeaderGenerator(ABC):

    def __init__(self, pathToFile: str): 
        
        if os.path.isfile(pathToFile):
            self.data = self._readFile(pathToFile)

        else:
            raise FileNotFoundError(f"{pathToFile} does not exist.")
        
        return

    def __call__(self, s: str) -> str:

        if s in self.data.keys(): 
            return rd.choice(self.data[s])
        else:
            raise ValueError('{s} is not implemented.')


    @staticmethod
    def _readFile(file:str, mode:str = 'r', encoding:str = 'utf-8') -> dict:
        """ Reads a .json file"""

        with open(file, mode, encoding = encoding) as f:
            data = json.load(f)

        return data

class Accept(HTTPHeaderGenerator):
    
    def __call__(self, browser):
        return self.data[browser]

class AcceptEncoding(HTTPHeaderGenerator):

    def __init__(self, pathToFile: str):

        super().__init__(pathToFile)
        self.data = self.data["Accept-Encoding"]

        return 

    def __call__(self, 
        qFactors: bool = True # Indicates if relative quality factors should be included
        ) -> str:
        """ Generates a random accept-encoding header tab """
        
        num      = rd.randint(1, len(self.data)) # Choose a random number <num> of encoding strings to be included in the header
        encoders = rd.sample(self.data, num)     # Make <k> unique random choices from the population of accepted encoders

        if '*' in encoders:     # Always set 'no preference' at the end
            encoders.pop(encoders.index('*')) 
            encoders.append('*')

        if 'gzip' in encoders:  # If 'gzip' is chosen put first  
            encoders.pop(encoders.index('gzip')) 
            encoders.insert(0, 'gzip')

        if qFactors:
            factors  = RelativeQualityFactorGenerator(len(encoders))
            encoders = [e + f for e, f in zip(encoders, factors)]

        return ", ".join(encoders)

class AcceptLanguage(HTTPHeaderGenerator):
    """ Generates a random language header tab """

    @staticmethod
    def _makeLanguageList(
        domain : str,  # Domain related language to be included
        other  : list  # List of additional languages to be included
        ):
        """ Makes the full list of languages to be included in the string"""

        if other is None: 
            languages = [domain]
            
        else:
            
            languages = other
            if domain not in languages: 
                languages.append(domain)

        return languages
    

    def __call__(self, 
        domain    : str,           # Domain to relate languages to
        universal : list = None,   # Languages that are always accepted. Set to None to deactivate
        qFactors  : bool = True    # Indicates if relative quality factors should be included
        ) -> str:

        # Get a language related to the current domain
        # Below will fail for generic domains (.info, .edu) (they don't have strict language requirements)
        # If it does, select an EU language randomly and return one of its domains
        try:    domLang = super().__call__(domain)
        except: domLang = super().__call__("eu")

        # Make languages list.
        languages = self._makeLanguageList(domLang, universal)

        if qFactors: # Add relative quality factors
            factors   = RelativeQualityFactorGenerator(len(languages))
            languages = [e + f for e, f in zip(languages, factors)]

        return ",".join(languages)

