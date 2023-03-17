""" This module implements the HeaderGenerator object for a request """

from abc         import ABCMeta
from typing      import Literal, Any, get_args
from definitions import DEVICE_TYPE, BROWSER_TYPE, DOMAIN_TYPE
import random as rd
import json

import os


def readFile(pathToFile: str) -> Any:
    """ Generic txt/json reader """

    isjson = lambda x: x.endswith('.json')
    istxt  = lambda x: x.endswith('.txt')

    if os.path.isfile(pathToFile):
        with open(pathToFile, mode = 'r', encoding = 'utf-8') as f:

            if   isjson(pathToFile): contents = json.load(f)
            elif istxt(pathToFile) : contents = f.readlines()
            else: raise RuntimeError(f"{pathToFile} is not a .json or .txt file")

    else:
        raise FileNotFoundError(f"{pathToFile} does not exist.")

    return contents


class Singleton(ABCMeta):
    """ Singleton metaclass """
    _instances = {}

    def __call__(cls, *args, **kwargs):

        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]


class Selector():
    """ Selects an os, device, and browser based on actual usage
        information obtained from https://gs.statcounter.com/
    """

    def __init__(self):
        """ Imports required data. """
        
        self.softwareData = readFile('./data/software_market_share.json')
        
        # Extract weights for device selection
        self.devices    = get_args(DEVICE_TYPE)
        self.devWeights = [self.softwareData[d]["usage"] for d in self.devices]

        # Extract weights for domain selection
        domainData      = readFile('./data/domain_market_share.json')
        self.domains    = get_args(DOMAIN_TYPE)
        self.domWeights = [domainData.get(domain, 1e-9) for domain in self.domains]
        # NOTE: If a domain is not available in the domain statistics file (./data/domain_market_share.json) 
        # it can still be selected with a low probability (=1e-9 - two orders of magnitude below the minimum on the file).
        
        return
    

    def __call__(self, 
        request: Literal['browser', 'device', 'domain'], **kwargs
        ) -> str:
        """ """

        if request == 'browser': return self._getBrowser(device = kwargs.get('device', 'desktop')) # assume desktop
        if request == 'device' : return self._getDevice()
        if request == 'domain' : return self._getDomain()


    def _getDevice(self) -> DEVICE_TYPE:
        """ Selects a device """
        return rd.choices(population = self.devices, weights = self.devWeights)[0]


    def _getBrowser(self, device: DEVICE_TYPE) -> BROWSER_TYPE:
        """ Selects a browser """

        browser = rd.choices(
            population = list( self.softwareData[device]["browser"].keys() ),
            weights    = list( self.softwareData[device]["browser"].values() )
        )[0]
        
        return browser


    def _getDomain(self) -> DOMAIN_TYPE:
        """ Selects a domain """
        return rd.choices(population = self.domains, weights = self.domWeights)[0]