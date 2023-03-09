""" This module implements the user agent Reader class, which generates user agents
    read from an input file.
"""

import os
from .generator    import BaseGenerator
from collections   import defaultdict
from typing        import Tuple, get_args
from .definitions  import BROWSER_TYPE


class Reader(BaseGenerator):
    """ Read user agents from a file. It is assumed that each 
        line of the file corresponds to a single user agent string.
    """

    def __init__(self, filename: str):
        """ Initialisation method. Parses the input file if it exists. """

        super().__init__()

        # Check if file exists and parse it
        if not os.path.isfile(filename):
            raise FileNotFoundError(f'File {filename} does not exist.')
        
        self.userAgents, self.browsers = self._getUserAgents(filename)

        return


    def _getUserAgents(self, filename: str) -> Tuple[dict, list]:
        """ Reads a list of User-Agent strings from a given file. """
        
        # Load file in memory
        with open(filename, 'r') as f: agents = f.readlines()
        
        # Remove leading/trailing spaces
        agents = [agent.strip()for agent in agents] 

        # Dictionary to hold user agents. It's structure is the following:
        # key: <browser name, device type> (both lowecased), value: user agent string
        agentDict = defaultdict(list)
        browsers  = [] # List of corresponding browsers

        for i, agent in enumerate(agents):

            # Extract operating system. If no OS is returned, set to
            # other, which will default to a 'desktop' device type.
            osName  = self.parser.get(agent, ('os', 'name'), 'windows').lower()
                
            # Get device type (assume desktop if no device type is returned)
            devType = self.osTypes.get(osName, 'desktop')

            # Extract browser name. If no name is returned, set to 'other'
            browser = self.parser.get(agent, ('browser', 'name'), 'other').lower()
            
            # If the browser has an acceptable name, store the data
            if browser in get_args(BROWSER_TYPE):
            
                agentDict[browser, devType].append(agent)
                browsers.append(browser)

        # Check if at least a user agent has been succesfully identified
        # If not, all user agents in the input file come from a browser 
        # that is not supported
        if not browsers:
            raise NotImplementedError(f'File {filename} does not contain any supported browsers.')
        
        return agentDict, browsers
    
