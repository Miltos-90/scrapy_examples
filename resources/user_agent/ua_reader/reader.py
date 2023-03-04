import os
from random import choice
from ..templates       import UserAgent
from ..ua_client_hints import ClientHintGenerator as CH
from ..ua_parser       import Parser 

class Reader():
    """ Read user agents from a file. It is assumed that each 
        line of the file corresponds to a single user agent string.
    """

    def __init__(self, filename: str):

        # Check if file exists
        if not os.path.isfile(filename):
            raise FileNotFoundError(f'File {filename} does not exist.')
        
        # Load file in memory
        with open(filename, 'r') as f: x = f.readlines()
        
        # Remove leading/trailing spaces
        self.agents = [e.strip()for e in x] 

        # Instantiate parser
        self.parser = Parser()

        return

    # Return a randomly selected user agent
    def __call__(self,
        deviceType  : str = 'desktop', # Device type
        browserName : str = None,      # Browser name
        ) -> UserAgent:

        ua      = UserAgent
        ua.name = choice(self.agents)
        
        # Parse it
        ua.browser, ua.cpu, ua.device, ua.engine, ua.os = self.parser(ua.name) 
        
        # Get User agent hints
        ua.clientHints = CH(ua.browser, ua.cpu, ua.device, ua.os)
        
        return ua 
