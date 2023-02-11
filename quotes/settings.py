import logging

# Scrapy settings for quotes project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

# General spider/bot settings
BOT_NAME         = 'quotes'
ALLOWED_DOMAINS  = ['quotes.toscrape.com']                
START_URLS       = ['https://quotes.toscrape.com/page/1/'] 
SPIDER_MODULES   = ['quotes.spiders']
NEWSPIDER_MODULE = 'quotes.spiders'
ROBOTSTXT_OBEY   = True 

# Configure logging
LOG_FILE         = 'logger.log'
LOG_FORMAT       = '%(levelname)s: %(message)s'
LOG_LEVEL        = logging.DEBUG

# Disable cookies (enabled by default)
COOKIES_ENABLED  = False

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES   = {
    'quotes.pipelines.UrlManagementPipeline': 0,
    'quotes.pipelines.DefaultValuesPipeline': 1,
    'quotes.pipelines.SaveQuotesPipeline'   : 2,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'quotes.middlewares.UrlManagementMiddleware': 0,
}

# Enable or disable extensions and related settings
# See https://docs.scrapy.org/en/latest/topics/extensions.html
EXTENSIONS = {
    'quotes.extensions.ProgressMonitor': 0,
}

PROGRESS_MONITOR_ENABLED = True
PROGRESS_MONITOR_STEP    = 10


# Database-related settings
DB_FILE     = "./scrapy_quotes.db"
URL_DB_FILE = "./visited_urls.db" 

DB_PRAGMA = """
    PRAGMA foreign_keys=ON;
    PRAGMA journal_mode=WAL;
    PRAGMA synchronous=FULL;
    """

URL_DB_PRAGMA = DB_PRAGMA

DB_SCHEMA = """
    -- Author data
    CREATE TABLE IF NOT EXISTS authors (
        id          INTEGER PRIMARY KEY,
        name        TEXT    UNIQUE NOT NULL,
        birthdate   TEXT    NOT NULL,
        birthplace  TEXT    NOT NULL,
        bio         TEXT    NOT NULL
    ) STRICT;

    -- Quote data
    CREATE TABLE IF NOT EXISTS quotes (
        id          INTEGER PRIMARY KEY,
        quote       TEXT    UNIQUE NOT NULL,
        tags        TEXT    NOT NULL,
        author_id   INTEGER NOT NULL,
        FOREIGN KEY(author_id)  REFERENCES authors(id)
    ) STRICT; 
"""

URL_DB_SCHEMA = """
    CREATE TABLE IF NOT EXISTS pages (
            id     INTEGER  PRIMARY KEY,
            url    TEXT     NOT NULL UNIQUE,
            date   TEXT     NOT NULL
        );
"""

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'quotes (+http://www.yourdomain.com)'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'quotes.middlewares.QuotesSpiderMiddleware': 543,
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
