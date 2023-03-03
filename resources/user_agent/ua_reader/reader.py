import os
from random import choice

class Reader():
    """ Simpe class to read user agents from a file. It is assumed that each 
        line of the filename corresponds to a single user agent string.
    """

    def __init__(self, filename: str):

        if not os.path.isfile(filename):
            raise FileNotFoundError(f'File {filename} does not exist.')
        
        with open(filename, 'r') as f: x = f.readlines()
        
        self.agents = [e.strip()for e in x] # Remove leading/trailing spaces

        return

    # Return a randomly selected user agent
    def __call__(self) -> str: return choice(self.agents)
