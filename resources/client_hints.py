""" Deriviation of user agent client hints based on a parsed user agent.
    See:https://github.com/WICG/ua-client-hints for definitions.
"""

from typing       import Dict
from utils        import readFile
from ua_generator import CHParser
from definitions  import EMPTY


class ClientHintGenerator():
    """ Generates user agent client hints from a user agent string. """

    def __init__(self):
        """ Initialisation method. Reads data and instantiates classes. """

        self.cpuBitness = readFile('./data/cpu_bitness.json')
        self.Parser     = CHParser()

        return


    def __call__(self, userAgent: str) -> Dict[str, str]:
        """ Generates client hints from a user agent, using the dictionaries
            resulting from the parsing operation.
        """

        # Parse user agent
        browser, cpu, device, _, os = self.Parser(userAgent)
        
        # Extract specific attributes needed
        bName     = getattr(browser, 'name')
        bVersion  = getattr(browser, 'version')
        bMajorVer = getattr(browser, 'majorVersion')
        cpuArch   = getattr(cpu,     'architecture')
        devType   = getattr(device,  'type')
        devModel  = getattr(device,  'model')
        osName    = getattr(os,      'name')
        osVersion = getattr(os,      'version')
        
        # Generate client hints dictionary
        return {
            "Sec-CH-UA"                   : self._UA(bName, bMajorVer),
            "Sec-CH-UA-Arch"              : self._UAGeneric(cpuArch),
            "Sec-CH-UA-Bitness"           : self._UABitness(cpuArch),
            "Sec-CH-UA-Full-Version-List" : self._UA(bName, bVersion, full = True),
            "Sec-CH-UA-Mobile"            : self._UAMobile(devType),
            "Sec-CH-UA-Model"             : self._UAGeneric(devModel),
            "Sec-CH-UA-Platform"          : self._UAPlatform(osName),
            "Sec-CH-UA-Platform-Version"  : self._UAGeneric(osVersion),
        }

        
    def _UABitness(self,
        name : str, # CPU architecture
        ) -> str:
        """ Generates the value of the Sec-CH-UA-Bitness header.
            See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-CH-UA-Bitness
        """
        
        return self._format(self.cpuBitness.get(name, EMPTY))


    def _UAGeneric(self,
        architecture: str # CPU architecutre
        ) -> str:
        """ Generates the value of the Sec-CH-UA-Arch, Sec-CH-UA-Model, Sec-CH-UA-Platform-Version headers.
            See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-CH-UA-Arch
                https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-CH-UA-Model
                https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-CH-UA-Platform-Version
        """

        return self._format(architecture)


    @staticmethod
    def _UAMobile(
        s: str # Device type
        ) -> str:
        """ Generates the value of the Sec-CH-UA-Mobile header.
            See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-CH-UA-Mobile
        """
            
        if s == 'mobile': return '?1'
        else            : return '?0'


    def _UAPlatform(self,
        name # Name of the operating system
        ) -> str:
        """ Generates the value of the Sec-CH-UA-Platform header.
            See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-CH-UA-Platform
        """
        
        if name.lower() not in ['ios', 'mac os', 'macos']: 
            name = name.title()

        return self._format(name)


    def _UA(self,
        name    : str,  # Brand name
        version : str,  # Major (Significant) version of the browser
        full    : bool = False
        ) -> str: 
        """ Generates the value of the Sec-CH-UA and Sec-CH-UA-Full-Version-List headers.
            See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-CH-UA
            and  https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-CH-UA-Full-Version-List
        """

        brandList = []
        if name != EMPTY: brandList.append({'brand': name, 'version': version})

        # Make  intentionally incorrect brand string
        if full : brandList.append({'brand': ' Not A;Brand', 'version': '99.0.0.0'})
        else    : brandList.append({'brand': ' Not A;Brand', 'version': '99'})

        # Convert to string
        return self._makeBrandString(brandList)


    @staticmethod
    def _makeBrandString(
        brandList: list # List of dicts {brand, version}
        ) -> str:
        """ Generates a string from the brand list of the user"""

        serial = []
        for d in brandList:
            brand   = d['brand']
            version = d['version']
            bLower  = brand.lower()

            if bLower == 'chrome':
                for name in ['Chromium', 'Google Chrome']:
                    serial.append(f'"{name}";v="{version}"')
            
            elif bLower == 'edge':
                for name in ['Chromium', 'Microsoft Edge']:
                    serial.append(f'"{name}";v="{version}"')

            else:
                # NOTE: If brand is not chrome or edge, this header is not supported (up until now, March 2023)
                # The following will simply append the brand name of the browser, but this header is 
                # going to be removed in the removeUnsupportedHeaders() function downstream.
                serial.append(f'"{brand}";v="{version}"')
        
        return ', '.join(serial)


    @staticmethod
    def _format(x: str) -> str:
        """ Generic string formatter for the client hints """
        
        return f'"{x}"'
