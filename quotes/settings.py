import logging
from utils.helpers import LoggerFilter
from scrapy.utils.log import configure_logging 

""" General spider/bot settings """
BOT_NAME               = 'quotes'
ALLOWED_DOMAINS        = ['quotes.toscrape.com']                
START_URLS             = ['https://quotes.toscrape.com/page/1/'] 
SPIDER_MODULES         = ['quotes.spiders']
NEWSPIDER_MODULE       = 'quotes.spiders'
CUSTOM_SPIDER_SETTINGS = {'JOBDIR': './crawls'}

""" Configure a delay for requests for the same website """
RANDOMIZE_DOWNLOAD_DELAY        = True 
DOWNLOAD_DELAY                  = 0.1  # Time [sec] to wait before downloading consecutive pages from the same website.
DOWNLOAD_TIMEOUT                = 30   # Time [sec] that the downloader will wait before timing out.
CONCURRENT_REQUESTS_PER_DOMAIN  = 16   # maximum number of concurrent requests performed to a single domain.

""" Logger configuration """
LOG_FILE        = './logger.log'
LOG_FORMAT      = '%(levelname)s: %(message)s'
LOG_LEVEL       = logging.DEBUG
COOKIES_ENABLED = True # Disable cookies (enabled by default

""" Item pipeline configuration"""
ITEM_PIPELINES = {
    'quotes.pipelines.DefaultValuesPipeline': 1,
    'quotes.pipelines.SavePipeline' : 2,
}

""" Spider middleware configuration """
SPIDER_MIDDLEWARES = {
   'scrapy.spidermiddlewares.referer.RefererMiddleware': 10,
}

""" Downloader middleware configuration """
DOWNLOADER_MIDDLEWARES = {
    'utils.middlewares.IPSwitchMiddleware': 450,
    'utils.middlewares.HeadersMiddleware': 650,
    'utils.middlewares.URLLoggerMiddleware': 950
}

# Retrying failed requests
RETRY_ENABLED    = True
RETRY_TIMES      = 5
RETRY_HTTP_CODES = [400, 500, 502, 503, 504, 522, 524, 408, 429]

# Tor handler 
TOR_ENABLED     = True
IP_CHANGE_CODES = RETRY_HTTP_CODES
IP_SETTLE_TIME  = 2 # Wait time for the new IP to "settle in"

# Header generator - see random_header_generator package
REFERER_ENABLED          = True
HEADER_GENERATOR_ENABLED = True
REFERRER_POLICY          = 'same-origin'
HEADER_DEVICE_TYPE       = 'desktop' 
HEADER_BROWSER_NAME      = None
HEADER_HTTP_VERSION      = 1
USER_AGENTS              = 'program'

# URL Logger
URL_LOG_ENABLED = True
URL_LOG_DB      = "./url_logger.db"

""" Extensions configuration """
EXTENSIONS  = {'utils.extensions.ProgressMonitor': 0}
PROGRESS_MONITOR_ENABLED = True
PROGRESS_MONITOR_STEP    = 10

""" Database-related settings """
DB   = "./scrapy_quotes.db"

DB_PRAGMA = """
    PRAGMA foreign_keys=OFF;
    PRAGMA journal_mode=WAL;
    PRAGMA synchronous=FULL;
    """

DB_SCHEMA = """
    -- Quote data
    CREATE TABLE IF NOT EXISTS quotes (
        id          INTEGER PRIMARY KEY,
        quote       TEXT    NOT NULL UNIQUE,
        keywords    TEXT    NOT NULL,
        author      TEXT    NOT NULL
    ) STRICT;

    -- Author data
    CREATE TABLE IF NOT EXISTS authors (
        id          INTEGER PRIMARY KEY,
        name        TEXT    NOT NULL UNIQUE,
        birthdate   TEXT    NOT NULL,
        birthplace  TEXT    NOT NULL,
        bio         TEXT    NOT NULL
    ) STRICT; 
"""

""" Apply logger configuration """
configure_logging(settings = {"LOG_FILE": LOG_FILE, "LOG_FORMAT": LOG_FORMAT, "LOG_LEVEL": LOG_LEVEL})
logging.getLogger('scrapy.core.scraper').addFilter(LoggerFilter())

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
