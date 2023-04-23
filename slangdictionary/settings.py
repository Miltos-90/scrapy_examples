import logging
from utils.helpers import LoggerFilter
from scrapy.utils.log import configure_logging 


""" General spider/bot settings """
CLOSESPIDER_ITEMCOUNT   = 0 # Default: 0
CLOSESPIDER_TIMEOUT     = 0 # Default: 0 [sec]
CLOSESPIDER_PAGECOUNT   = 0 # Default: 0
BOT_NAME                = "slangdictionary"
SPIDER_MODULES          = ["slangdictionary.spiders"]
NEWSPIDER_MODULE        = "slangdictionary.spiders"
ALLOWED_DOMAINS         = ['onlineslangdictionary.com']                
START_URLS              = ['http://onlineslangdictionary.com/word-list/0-a/']
CUSTOM_SPIDER_SETTINGS  = {'JOBDIR': './crawls'}
ROBOTSTXT_OBEY          = False

""" Configure a delay for requests for the same website """
RANDOMIZE_DOWNLOAD_DELAY        = True 
DOWNLOAD_DELAY                  = 0.1  # Time [sec] to wait before downloading consecutive pages from the same website.
DOWNLOAD_TIMEOUT                = 30   # Time [sec] that the downloader will wait before timing out.
CONCURRENT_REQUESTS_PER_DOMAIN  = 16   # maximum number of concurrent requests performed to a single domain.


""" Item pipeline configuration"""
ITEM_PIPELINES = {
    "slangdictionary.pipelines.DefaultValuesPipeline": 300,
    "slangdictionary.pipelines.SavePipeline": 310,
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
DB   = "./slang_dict.db"

DB_PRAGMA = """
    PRAGMA foreign_keys=OFF;
    PRAGMA journal_mode=WAL;
    PRAGMA synchronous=FULL;
    """

DB_SCHEMA = """
    CREATE TABLE IF NOT EXISTS items (
        id              INTEGER PRIMARY KEY,
        word            TEXT NOT NULL,
        definition      TEXT NOT NULL,
        users_used      INTEGER,
        users_not_used  INTEGER,
        users_heard     INTEGER,
        users_not_heard INTEGER,
        vulgarity       INTEGER
    ) STRICT; 
"""

""" Logger configuration """
LOG_FILE   = './logger.log'
LOG_FORMAT = '%(levelname)s: %(message)s'
LOG_LEVEL  = logging.ERROR
configure_logging(settings = {"LOG_FILE": LOG_FILE, "LOG_FORMAT": LOG_FORMAT, "LOG_LEVEL": LOG_LEVEL})
logging.getLogger('scrapy.core.scraper').addFilter(LoggerFilter())

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR      = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
