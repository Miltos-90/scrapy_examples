# ===============================================================
def clean(paths: list):
    import os
    import shutil
    for p in paths:
        if os.path.isfile(p): os.remove(p)
        if os.path.isdir(p) : shutil.rmtree(p)
    
    return
# ===============================================================

clean(paths = ['./logger.log', './scrapy_quotes.db', './url_logger.db', './crawls'])

from quotes.spiders.spider import QuotesSpider
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess

process = CrawlerProcess(get_project_settings())
process.crawl(QuotesSpider)
#process.crawl(AnotherSpider) ... Run multiple spiders here if needed
process.start()