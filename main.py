# ===============================================================
def clean(paths: list):
    import os
    import shutil
    for p in paths:
        if os.path.isfile(p): os.remove(p)
        if os.path.isdir(p) : shutil.rmtree(p)
    
    return
# ===============================================================

clean(paths = ['./logger.log', './crawls'])

from slangdictionary.spiders.spider import SlangSpider
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess

process = CrawlerProcess(get_project_settings())
process.crawl(SlangSpider)
#process.crawl(AnotherSpider) ... Run multiple spiders here if needed
process.start()