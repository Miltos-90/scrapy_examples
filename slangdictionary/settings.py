# Scrapy settings for slangdictionary project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

CLOSESPIDER_ITEMCOUNT   = 0 # Default: 0
CLOSESPIDER_TIMEOUT     = 0 # Default: 0 [sec]
CLOSESPIDER_PAGECOUNT   = 150 # Default: 0
BOT_NAME                = "slangdictionary"
SPIDER_MODULES          = ["slangdictionary.spiders"]
NEWSPIDER_MODULE        = "slangdictionary.spiders"
ALLOWED_DOMAINS         = ['onlineslangdictionary.com']                
START_URLS              = ['http://onlineslangdictionary.com/meaning-definition-of/5-by-5']

# ['http://onlineslangdictionary.com/meaning-definition-of/3rd-base']
# ['http://onlineslangdictionary.com/word-list/0-a/']
# ['http://onlineslangdictionary.com/meaning-definition-of/1432']
# ['http://onlineslangdictionary.com/meaning-definition-of/as-useless-as-tits-on-a-boar-hog']
# ['http://onlineslangdictionary.com/meaning-definition-of/10%253a30'] 
# [http://onlineslangdictionary.com/meaning-definition-of/asshole]
# ['http://onlineslangdictionary.com/meaning-definition-of/1080']
CUSTOM_SPIDER_SETTINGS  = {'JOBDIR': './crawls'}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "slangdictionary (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "slangdictionary.middlewares.SlangdictionarySpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "slangdictionary.middlewares.SlangdictionaryDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "slangdictionary.pipelines.SlangdictionaryPipeline": 300,
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
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
