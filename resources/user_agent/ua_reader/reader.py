import os
from random            import choice
from ..templates       import UserAgent, OS_TYPES
from ..ua_client_hints import ClientHintGenerator as CH
from ..ua_parser       import Parser 
from collections       import defaultdict
from typing            import Tuple

class Reader():
    """ Read user agents from a file. It is assumed that each 
        line of the file corresponds to a single user agent string.
    """

    def __init__(self, filename: str):

        # Check if file exists
        if not os.path.isfile(filename):
            raise FileNotFoundError(f'File {filename} does not exist.')
        
        self.parser = Parser()

        self.userAgents, self.browsers = self.getUserAgents(filename)

        return


    def getUserAgents(self, filename: str) -> Tuple[dict, list]:
        """
        Reads a list of User-Agent strings from a given file.
        """
        
        # Load file in memory
        with open(filename, 'r') as f: agents = f.readlines()
        
        # Remove leading/trailing spaces
        agents = [agent.strip()for agent in agents] 

        # Dictionary to hold user agents. It's structure is the following:
        # key: <browser name, device type> (both lowecased), value: user agent string
        agentDict = defaultdict(list)
        browsers  = []

        for agent in agents:

            # Extract operating system. If no OS is returned, set to
            # other, which will default to a 'desktop' device type.
            osName  = self.parser.get(agent, ('os', 'name'), 'windows').lower()
                
            # Get device type (assume desktop if no device type is returned)
            devType = OS_TYPES.get(osName, 'desktop')

            # Extract browser name. If no name is returned, set to 'other'
            browser  = self.parser.get(agent, ('browser', 'name'), 'other').lower()
            
            agentDict[browser, devType].append(agent)
            browsers.append(browser)
        
        return agentDict, browsers
    

    # Return a randomly selected user agent
    def __call__(self,
        deviceType  : str = 'desktop', # Device type
        browserName : str = None,      # Browser name
        ) -> UserAgent:

        ua = UserAgent
        # Choose one at random if not provided
        if not browserName: browserName = choice(self.browsers) 

        # Get a randomly selected user agent string for the selected browser and device type
        applicableAgents = self.userAgents.get( (browserName, deviceType) )

        if applicableAgents:
            ua.name = choice(applicableAgents)

        else:
            # If nothing is found (due to invalid name/type combination), get a chrome/desktop
            # user agent.
            ua.name = choice(self.userAgents.get( ('desktop', 'chrome') ) )

        # Parse it
        ua.browser, ua.cpu, ua.device, ua.engine, ua.os = self.parser(ua.name) 
        
        # Get User agent hints
        ua.clientHints = CH(ua.browser, ua.cpu, ua.device, ua.os)
        
        return ua 
