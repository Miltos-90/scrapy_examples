""" Implementation of the user agent client hints according to:
    https://github.com/WICG/ua-client-hints
"""

from ua_client_hints.constants import CPUBitness

format = lambda x: f'"{x}"' if x else '""' # Generic string formatter for the User agent hints


def ClientHints(userAgent: dict) -> dict:
    """ Generates client hints from a parsed user agent. 
        Input is a dict containing the assigned fields of the user agent scraper
        (see: ./ua_scraper/scraper.py)
    """

    chDict = {
            'Sec-CH-UA'                   : _UA(
                userAgent['browser', 'name'], 
                userAgent['browser', 'major_version']
                ),
            'Sec-CH-UA-Arch'              : _UAGeneric(userAgent['cpu','architecture']),
            'Sec-CH-UA-Bitness'           : _UABitness(userAgent['cpu','architecture']),
            'Sec-CH-UA-Full-Version-List' : _UA(
                userAgent['browser', 'name'], 
                userAgent['browser', 'version'], 
                fullVersion = True
                ),
            'Sec-CH-UA-Mobile'            : _UAMobile(userAgent['device','type']),
            'Sec-CH-UA-Model'             : _UAGeneric(userAgent['device','model']),
            'Sec-CH-UA-Platform'          : _UAPlatform(userAgent['os','name']),
            'Sec-CH-UA-Platform-Version'  : _UAGeneric(userAgent['os', 'version'])
        }

    return chDict
    

def _UABitness(
    name     : str, # CPU architecture
    cpuToBit : dict = CPUBitness,
    ) -> str:
    """ Generates the value of the Sec-CH-UA-Bitness header.
        See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-CH-UA-Bitness
    """
    
    return format(cpuToBit.get(name))


def _UAGeneric(
    architecture: str # CPU architecutre
    ) -> str:
    """ Generates the value of the Sec-CH-UA-Arch, Sec-CH-UA-Model, Sec-CH-UA-Platform-Version headers.
        See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-CH-UA-Arch
             https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-CH-UA-Model
             https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-CH-UA-Platform-Version
    """

    return format(architecture)


def _UAMobile(
    s: str # Device type
    ) -> str:
    """ Generates the value of the Sec-CH-UA-Mobile header.
        See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-CH-UA-Mobile
    """
        
    if s == 'mobile':
        return '?1'
    else:
        return '?0'
    

def _UAPlatform(
    name # Name of the operating system
    ) -> str:
    """ Generates the value of the Sec-CH-UA-Platform header.
        See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-CH-UA-Platform
    """
    
    if name.lower() not in ['ios', 'mac os']: name = name.title()

    return format(name)


def _UA(
    name    : str, # Browser name
    version : str,  # Major (Significant) version of the browser
    fullVersion: bool = False
    ) -> str: 
    """ Generates the value of the Sec-CH-UA and Sec-CH-UA-Full-Version-List headers.
        See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-CH-UA
        and  https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-CH-UA-Full-Version-List
    """

    # Intentionally incorrect brand string
    if fullVersion  : default = {'brand': ' Not A;Brand', 'version': '99.0.0.0'}
    else            : default = {'brand': ' Not A;Brand', 'version': '99'}

    # Make brand list
    brandList = [default, {'brand': name, 'version': version}]

    # Convert to string
    return _makeBrandString(brandList)


def _makeBrandString(
    brandList: list # List of dicts {brand, version}
    ) -> str:
    """ Generates a string from the brand list of the user"""

    serial = []
    for d in brandList:
        print(d)
        brand   = d['brand']
        version = d['version']
        serial.append(f'"{brand}";v="{version}"')
    
    return ', '.join(serial)
