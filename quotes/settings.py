import logging

# Scrapy settings for quotes project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

""" General spider/bot settings """
CLOSESPIDER_ITEMCOUNT = 0 # Default: 0
CLOSESPIDER_TIMEOUT   = 0 # Default: 0 [sec]
CLOSESPIDER_PAGECOUNT = 0 # Default: 0
BOT_NAME              = 'quotes'
ALLOWED_DOMAINS       = ['quotes.toscrape.com']                
START_URLS            = ['https://quotes.toscrape.com/page/1/'] 
SPIDER_MODULES        = ['quotes.spiders']
NEWSPIDER_MODULE      = 'quotes.spiders'
ROBOTSTXT_OBEY        = True 

""" Configure a delay for requests for the same website """
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY           = 0     # Time [sec] to wait before downloading consecutive pages from the same website. (Default = 0)
RANDOMIZE_DOWNLOAD_DELAY = False # Random time in [0.5 * DOWNLOAD_DELAY and 1.5 * DOWNLOAD_DELAY] to wait while fetching requests from the same website.
DOWNLOAD_TIMEOUT         = 30    # Time [sec] that the downloader will wait before timing out. (Default = 160)

# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 16 # maximum number of concurrent requests performed to a single domain.
#CONCURRENT_REQUESTS = 32 # maximum concurrent requests performed by Scrapy (default: 16)

""" Logger configuration """
LOG_FILE         = './logger.log'
LOG_FORMAT       = '%(levelname)s: %(message)s'
LOG_LEVEL        = logging.DEBUG
COOKIES_ENABLED  = False # Disable cookies (enabled by default

""" Request filter configuration """
DUPEFILTER_CLASS = 'scrapy.dupefilters.BaseDupeFilter' # Disable duplicate URL filter

""" Item pipeline configuration"""
# Configure item pipelines (See https://docs.scrapy.org/en/latest/topics/item-pipeline.html)
ITEM_PIPELINES   = {
    'quotes.pipelines.DefaultValuesPipeline': 1,
    'quotes.pipelines.SaveQuotesPipeline'   : 2,
}

""" Downloader middleware configuration """
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'quotes.middlewares.RandomRequestHeadersMiddleware': 400,
    'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': None, # Set to none for random headers
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware':           None, # Set to none for random headers
}

# Retrying failed requests status
RETRY_ENABLED    = True
RETRY_TIMES      = 5
RETRY_HTTP_CODES = [400, 500, 502, 503, 504, 522, 524, 408, 429]

""" Request header configuration """
# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}
#USER_AGENT = 'quotes (+http://www.yourdomain.com)' # Crawl responsibly by identifying yourself (and your website) on the user-agent
NUM_REQUESTS_FOR_HEADER_CHANGE = 10
USER_AGENT_LIST = '../resources/request_headers/user_agent_database.txt'
REFERER_LIST    = '../resources/request_headers/referer_database.txt'

""" Extensions configuration """
# Enable or disable extensions and related settings (See https://docs.scrapy.org/en/latest/topics/extensions.html)
EXTENSIONS = {
    'quotes.extensions.ProgressMonitor': 0,
}

PROGRESS_MONITOR_ENABLED = True
PROGRESS_MONITOR_STEP    = 10

""" Database-related settings """
DB_FILE   = "./scrapy_quotes.db"
DB_PRAGMA = """
    PRAGMA foreign_keys=ON;
    PRAGMA journal_mode=WAL;
    PRAGMA synchronous=FULL;
    """
DB_SCHEMA = """
    -- Quote data
    CREATE TABLE IF NOT EXISTS quotes (
        id          INTEGER PRIMARY KEY,
        quote       TEXT    NOT NULL UNIQUE,
        tags        TEXT    NOT NULL,
        author_id   INTEGER NOT NULL,
        FOREIGN KEY(author_id)  REFERENCES authors(id)
    ) STRICT;

    -- Author data
    CREATE TABLE IF NOT EXISTS authors (
        id          INTEGER PRIMARY KEY,
        name        TEXT    NOT NULL UNIQUE,
        birthdate   TEXT    NOT NULL,
        birthplace  TEXT    NOT NULL,
        bio         TEXT    NOT NULL
    ) STRICT; 

    -- scraped pages schema
    CREATE TABLE IF NOT EXISTS pages (
            id            INTEGER  PRIMARY KEY,
            url           TEXT     NOT NULL UNIQUE,
            date          TEXT     NOT NULL,
            status_code   INTEGER  NOT NULL,
            crawl_success INTEGER  NOT NULL
        ) STRICT;
"""



# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False


# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#   'quotes.middlewares.QuotesSpiderMiddleware': 1,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
