from logging import Filter, getLogger
from scrapy.utils.log import configure_logging 
from scrapy.utils.project import get_project_settings

SETTINGS = get_project_settings()


""" Logger configuration """

class LoggerFilter(Filter):
    """ Filter that forbids scraped items to be logged """
    def filter(self, record):
        
        return not record.getMessage().startswith('Scraped from')

configure_logging(
    settings = {
                "LOG_FILE"   : SETTINGS.get("LOG_FILE"),
                "LOG_FORMAT" : SETTINGS.get("LOG_FORMAT"),
                "LOG_LEVEL"  : SETTINGS.get("LOG_LEVEL")
            }
        )

getLogger('scrapy.core.scraper').addFilter(LoggerFilter())
