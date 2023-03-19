
from abc    import ABC
from typing import Union
from utils  import readFile
import random as rd


class HTTPHeaderGenerator(ABC):
    """ Generic HTTP Header generator class """

    def __init__(self, pathToFile: str):
        """ Initialisation method. Reads necessary data. """
        
        self.data = readFile(pathToFile)
        
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
    def _addQFactors(l:list) -> list:
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


class Accept(HTTPHeaderGenerator):
    """ Generator of the 'Accept' header """

    def __call__(self, 
        name    : str,  # Browser name
        version : float # Browser major (significant) version
        ) -> str:
        """ Generate a randomized Accept Encoding header. """

        # Get header values corresponding to this browser, i.e.
        # a list of version-from and -to numbers [integers] and header contents
        list_ = self.data[name]

        # Loop over the list and get the header value according to the version range
        for dict_ in list_:
            if version >= dict_["version_from"] and version < dict_["version_to"]:
                return dict_["header"]
        
        # If this point is reached, the version was not found
        raise ValueError(f'{name} browser version {version} is not supported for the "Accept" header')


class AcceptEncoding(HTTPHeaderGenerator):
    """ Generator of the 'Accept-Encoding' header """

    def __init__(self, pathToFile: str):
        """ Initialisation method. Reads necessary data. """

        super().__init__(pathToFile)

        # The file contains a dict of a single element. Unpack it
        self.data = self.data["Accept-Encoding"]

        return 


    def __call__(self, 
        addQFactors: Union[bool, None] = None # Indicates if relative quality factors should be included
        ) -> str:
        """ Generate a randomized Accept Encoding header. """
        
        if not addQFactors: 
            addQFactors = rd.random() >= 0.5      # Choose randomly if quality factors will be included if not specified
        
        numStr   = rd.randint(1, len(self.data))  # Choose a random number <num> of encoding strings to be included
        encoders = rd.sample(self.data, numStr)   # Make <k> unique random choices from the population of accepted encoders

        if '*' in encoders:     # Always set 'no preference' at the end
            encoders.pop(encoders.index('*')) 
            encoders.append('*')

        if 'gzip' in encoders:  # If 'gzip' is chosen, put it first  
            encoders.pop(encoders.index('gzip')) 
            encoders.insert(0, 'gzip')

        # Add relative quality factors
        if addQFactors: encoders = self._addQFactors(encoders)

        return ", ".join(encoders)


class AcceptLanguage(HTTPHeaderGenerator):
    """ Generator of the 'Accept-Language' header """

    def __call__(self, 
        domain          : str,                              # Domain to relate languages to
        globalLanguages : list = ['en', 'en-GB', 'en-US'],  # Languages that are always accepted
        addQFactors     : Union[bool, None] = None          # Indicates if relative quality factors should be included
        ) -> str:
        """ Generate a randomized 'Accept-Language' header """

        # Get a language related to the input domain
        domainLanguage = super().__call__(domain, defaultKey = "eu")

        # Prevent the same language from appearing in both the domain-specific language and the universal languages
        dupe = domainLanguage in globalLanguages
        if not dupe : languages = [domainLanguage] + globalLanguages
        else        : languages = globalLanguages

        # Add relative quality factors
        if addQFactors: languages = self._addQFactors(languages)

        return ",".join(languages)

