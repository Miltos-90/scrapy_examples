from logging import Filter
from abc import ABCMeta


class LoggerFilter(Filter):
    """ Filter that forbids scraped items to be logged """

    def filter(self, record):
        return not record.getMessage().startswith('Scraped from')


class Singleton(ABCMeta):
    """ Singleton metaclass """
    _instances = {}

    def __call__(cls, *args, **kwargs):

        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]


class Scheduler(object):
    """ Schedules the rotation of IPs, user agents and headers"""

    def __init__(self, numIterations: int):
        """ Initialisation method """

        if numIterations <= 0: 
            raise ValueError("Only positive number of requests is allowed for header randomization.")
        
        self.numIterations = numIterations
        self.iterCounter   = 0 # Current iteration counter

        return

    def __call__(self):
        """ Shceduler for IP/header switching.
            Returns True if values should be changed, False otherwise
        """

        if self.iterCounter == self.numIterations or self.iterCounter == 0:
            self.iterCounter = 0 # Reset
            out = True
        else:
            out = False

        self.iterCounter += 1

        return out