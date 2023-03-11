""" This module implements the user agent Reader class, which generates user agents
    read from an input file.
"""
import sys
sys.path.append("../utils") # Adds higher directory to python modules path

from .generator   import BaseGenerator
from utils        import readFile


class Reader(BaseGenerator):
    """ Read user agents from a file. It is assumed that each 
        line of the file corresponds to a single user agent string.
    """

    def __init__(self, filename: str):
        """ Initialisation method. Parses the input file if it exists. """

        super().__init__()
        self._getUserAgents(filename)

        return


    def _getUserAgents(self, filename: str):
        """ Reads a list of User-Agent strings from a given file. """
        
        agents  = readFile(filename)
        agents  = [a.strip() for a in agents]
        [self._add(agent) for agent in agents]
        self._check()

        return 