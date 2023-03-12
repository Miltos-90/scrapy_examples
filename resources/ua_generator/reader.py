""" This module implements the user agent Reader class, which generates user agents
    read from an input file.
"""
import sys
sys.path.append("../utils") # Adds higher directory to python modules path
sys.path.append("../definitions") # Adds higher directory to python modules path

from .generator    import BaseGenerator
from utils         import readFile
from definitions   import MAX_USER_AGENT_SIZE


class Reader(BaseGenerator):
    """ Read user agents from a file. It is assumed that each 
        line of the file corresponds to a single user agent string.
    """

    def __init__(self, filename: str):
        """ Initialisation method. Parses the input file if it exists. """

        super().__init__()
        self._get(filename)

        return


    def _get(self, filename: str):
        """ Reads a list of User-Agent strings from a given file. """
        
        agents  = readFile(filename)
        
        for agent in agents:
            if len(agent.strip()) <= MAX_USER_AGENT_SIZE:
                self._add(agent) # Add to dictionary (see generator.py)

        self._check() # Check how many were imported

        return 