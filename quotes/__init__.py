from logging import getLogger
from quotes.helpers import LoggerFilter
from scrapy.utils.log import configure_logging 
from scrapy.utils.project import get_project_settings


""" Logger configuration """
SETTINGS = get_project_settings()

configure_logging(
    settings = {
        "LOG_FILE"   : SETTINGS.get("LOG_FILE"),
        "LOG_FORMAT" : SETTINGS.get("LOG_FORMAT"),
        "LOG_LEVEL"  : SETTINGS.get("LOG_LEVEL")
        }
    )

getLogger('scrapy.core.scraper').addFilter(LoggerFilter())
