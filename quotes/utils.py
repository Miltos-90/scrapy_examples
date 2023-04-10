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

