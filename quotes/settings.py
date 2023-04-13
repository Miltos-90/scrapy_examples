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
COOKIES_ENABLED  = True # Disable cookies (enabled by default

""" Request filter configuration """
DUPEFILTER_CLASS = 'scrapy.dupefilters.BaseDupeFilter' # Disable duplicate URL filter

""" Item pipeline configuration"""
# Configure item pipelines (See https://docs.scrapy.org/en/latest/topics/item-pipeline.html)
ITEM_PIPELINES   = {
    'quotes.pipelines.DefaultValuesPipeline': 1,
    'quotes.pipelines.SavePipeline'   : 2,
}

""" Spider middleware configuration """
SPIDER_MIDDLEWARES = {
   'scrapy.spidermiddlewares.referer.RefererMiddleware': 10,
}

""" Downloader middleware configuration """
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,
    'quotes.middlewares.IPSwitchMiddleware': 450,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 500,
    'scrapy.downloadermiddlewares.ajaxcrawl.AjaxCrawlMiddleware': 560,
    'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware': 580,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 590,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': 600,
    'quotes.middlewares.HeadersMiddleware': 650,
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 700,
    'scrapy.downloadermiddlewares.stats.DownloaderStats': 850,
    'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 900,
    'quotes.middlewares.URLLoggerMiddleware': 950
}

# Retrying failed requests status
RETRY_ENABLED    = True
RETRY_TIMES      = 5
RETRY_HTTP_CODES = [400, 500, 502, 503, 504, 522, 524, 408, 429]

# Tor handler 
TOR_ENABLED           = True
IP_CHANGE_CODES       = RETRY_HTTP_CODES
TOR_CONTROL_PORT      = 9051
TOR_PASSWORD          = 'miltos'
PRIVOXY_PROXY_ADDRESS = 'http://127.0.0.1:8118'
IP_SETTLE_TIME        = 2 # Wait time for the new IP to "settle in"

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
URL_LOG_SCHEMA  = """
    -- scraped pages schema
    CREATE TABLE IF NOT EXISTS pages (
            id            INTEGER PRIMARY KEY,
            url           TEXT    NOT NULL UNIQUE,
            date          TEXT    NOT NULL,
            status_code   INTEGER NOT NULL,
            fingerprint   TEXT    NOT NULL,
            IP_address    TEXT    NOT NULL,
            server_name   TEXT    NOT NULL,
            locale        TEXT    NOT NULL,
            referer       TEXT    NOT NULL,
            user_agent    TEXT    NOT NULL,
            down_latency  REAL    NOT NULL
        ) STRICT;
"""


""" Extensions configuration """
# Enable or disable extensions and related settings (See https://docs.scrapy.org/en/latest/topics/extensions.html)
EXTENSIONS = {
    'quotes.extensions.ProgressMonitor': 0,
}

PROGRESS_MONITOR_ENABLED = True
PROGRESS_MONITOR_STEP    = 10

""" Database-related settings """
DB   = "./scrapy_quotes.db"
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



# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False




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
