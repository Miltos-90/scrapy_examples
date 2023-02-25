""" Implementation of the user agent client hints according to:
    https://github.com/WICG/ua-client-hints#should-the-ua-string-be-a-set
"""

from ua_generator.data import osTypes as OS_TYPES


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


def chArch() -> str:
    """ Generates the value of the Sec-CH-UA-Arch header.
        See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-CH-UA-Arch
    """
    # TODO
    return


def chBitness() -> str:
    """ Generates the value of the Sec-CH-UA-Bitness header.
        See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-CH-UA-Bitness
    """
    # TODO
    return


def chModel(modelName: str) -> str:
    """ Generates the value of the Sec-CH-UA-Model header.
        See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-CH-UA-Model
    """
    # TODO
    return f'"{modelName}"' if modelName is not None else '""'


def _chMobile(name):
    """ Generates the value of the Sec-CH-UA-Mobile header.
        See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-CH-UA-Mobile
    """
        
    if OS_TYPES[name] == 'mobile':
        return '?1'
    else:
        return '?0'
    

def _chPlatform(
    name # Name of the operating system
    ) -> str:
    """ Generates the value of the Sec-CH-UA-Platform header.
        See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-CH-UA-Platform
    """

    if   name == 'ios'  : platform = 'iOS'
    elif name == 'macos': platform = 'macOS'
    else                : platform = name.title()

    return f'"{platform}"'


def _chPlatformVersion(
    version: str # Full version of the operating system
    ) -> str: 
    """ Generates the value of the Sec-CH-UA-Platform-Version header.
        See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-CH-UA-Platform-Version
    """
    return f'"{version}"'


def _chUA(
    name    : str, # Browser name
    version : str  # Major (Significant) version of the browser
    ) -> str: 
    """ Generates the value of the Sec-CH-UA header.
        See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-CH-UA
    """

    version = version.split('.', 1)[0]                   # Keep the leftmost part of the number
    default = {'brand': ' Not A;Brand', 'version': '99'} # Intentionally incorrect brand string
        
    if name == 'chrome':
        brandList = [
            default,
            {'brand': 'Chromium',      'version': version},
            {'brand': 'Google Chrome', 'version': version}
            ]

    elif name == 'edge':
        brandList = [
            default,
            {'brand': 'Chromium',       'version': version},
            {'brand': 'Microsoft Edge', 'version': version}
        ]

    return _makeBrandString(brandList)


def _makeBrandString(
    brandList: list # List of dicts {brand, version}
    ) -> str:
    """ Generates a string from the brand list of the user"""

    serial = []
    for d in brandList:
        brand   = d['brand']
        version = d['version']
        serial.append(f'"{brand}";v="{version}"')
    
    return ', '.join(serial)
