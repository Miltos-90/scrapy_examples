""" Implementation of the user agent client hints according to:
    https://github.com/WICG/ua-client-hints#should-the-ua-string-be-a-set
"""


def chBitness() -> str:
    """ Generates the value of the Sec-CH-UA-Bitness header.
        See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-CH-UA-Bitness
    """
    # TODO
    return


def UAArch(
    architecture: str # CPU architecutre
    ) -> str:
    """ Generates the value of the Sec-CH-UA-Arch header.
        See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-CH-UA-Arch
    """

    return f'"{architecture}"' if architecture is not None else '""'


def UAModel(modelName: str) -> str:
    """ Generates the value of the Sec-CH-UA-Model header.
        See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-CH-UA-Model
    """
    # TODO
    return f'"{modelName}"' if modelName is not None else '""'


def UAMobile(
    s: str # Device type
    ) -> str:
    """ Generates the value of the Sec-CH-UA-Mobile header.
        See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-CH-UA-Mobile
    """
        
    if s == 'mobile':
        return '?1'
    else:
        return '?0'
    

def UAPlatform(
    name # Name of the operating system
    ) -> str:
    """ Generates the value of the Sec-CH-UA-Platform header.
        See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-CH-UA-Platform
    """

    if   name == 'ios'  : platform = 'iOS'
    elif name == 'macos': platform = 'macOS'
    else                : platform = name.title()

    return f'"{platform}"'


def UAPlatformVersion(
    version: str # Full version of the operating system
    ) -> str: 
    """ Generates the value of the Sec-CH-UA-Platform-Version header.
        See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-CH-UA-Platform-Version
    """
    return f'"{version}"'

def UA(
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
