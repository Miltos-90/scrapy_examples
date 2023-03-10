""" Deriviation of user agent client hints based on a parsed user agent.
    See:https://github.com/WICG/ua-client-hints for definitions.
"""

import sys
sys.path.append(".../utils") # Adds higher directory to python modules path (allows utils.py importing)

from .definitions import ClientHints, Browser, CPU, Device, OS
from typing       import Union
from utils        import readFile

CPU_BITNESS = readFile('./data/cpu_bitness.json') # Read CPU Bitness mapper

def ClientHintGenerator(browser: Browser, cpu: CPU, device: Device, os: OS) -> ClientHints:
    """ Generates client hints from a parsed user agent, using the dictionaries
        resulting from the parsed operation. Their definitions are found in the 
        user_agent.utils.py file
    """

    return ClientHints(
        Sec_CH_UA                   = _UA(browser.get('name'), browser.get('majorVersion')),
        Sec_CH_UA_Arch              = _UAGeneric(cpu.get('architecture')),
        Sec_CH_UA_Bitness           = _UABitness(cpu.get('architecture')),
        Sec_CH_UA_Full_Version_List = _UA(browser.get('name'), browser.get('version'), fullVersion = True),
        Sec_CH_UA_Mobile            = _UAMobile(device.get('type')),
        Sec_CH_UA_Model             = _UAGeneric(device.get('model')),
        Sec_CH_UA_Platform          = _UAPlatform(os.get('name')),
        Sec_CH_UA_Platform_Version  = _UAGeneric( os.get('version')),
        )
    

def _UABitness(
    name : str, # CPU architecture
    mapper: dict = CPU_BITNESS
    ) -> str:
    """ Generates the value of the Sec-CH-UA-Bitness header.
        See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-CH-UA-Bitness
    """
    
    return _format(mapper.get(name))


def _UAGeneric(
    architecture: str # CPU architecutre
    ) -> str:
    """ Generates the value of the Sec-CH-UA-Arch, Sec-CH-UA-Model, Sec-CH-UA-Platform-Version headers.
        See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-CH-UA-Arch
             https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-CH-UA-Model
             https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-CH-UA-Platform-Version
    """

    return _format(architecture)


def _UAMobile(
    s: str # Device type
    ) -> str:
    """ Generates the value of the Sec-CH-UA-Mobile header.
        See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-CH-UA-Mobile
    """
        
    if s == 'mobile': return '?1'
    else            : return '?0'
    

def _UAPlatform(
    name # Name of the operating system
    ) -> str:
    """ Generates the value of the Sec-CH-UA-Platform header.
        See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-CH-UA-Platform
    """
    
    if name is not None and name.lower() not in ['ios', 'mac os']: 
        name = name.title()

    return _format(name)


def _UA(
    name    : str,  # Brand name
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
    brandList = [default]
    if name is not None:
        brandList.append({'brand': name, 'version': version})

    # Convert to string
    return _makeBrandString(brandList)


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


# Generic string formatter for the client hints
def _format(x: Union[str, None]): return f'"{x}"' if x else '""'
