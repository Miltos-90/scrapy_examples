# scrapy startproject abbreviation_scraper
# scrapy crawl quotes -o quotes.jsonl:jsonlines
# More examples and patterns: https://docs.scrapy.org/en/latest/intro/tutorial.html#intro-tutorial


# https://datawookie.dev/blog/2021/06/scrapy-rotating-tor-proxy/
# https://medium.com/hackernoon/web-scraping-tutorial-with-python-tips-and-tricks-db070e70e071
# https://scrapeops.io/web-scraping-playbook/web-scraping-guide-header-user-agents/#ensuring-proper-header-order


# ===============================================================
def clean():
    import os
    import shutil
    paths = ['./logger.log', './scrapy_quotes.db', './url_logger.db']
    for filePath in paths:
        if os.path.isfile(filePath): 
            os.remove(filePath)
    
    shutil.rmtree('./crawls')


# ===============================================================


clean()

# When clean is commented out, the extension reports wrong number of items for some reason.
from quotes.spiders.ifconfig_spider import IfconfigSpider
from quotes.spiders.quotes_spider import QuotesSpider
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess


process = CrawlerProcess(get_project_settings())
process.crawl(QuotesSpider)
#process.crawl(QuotesSpider2) ... Run multiple spiders here if needed
process.start() # the script will block here until all crawling jobs are finished

# TODO: Finish header middleware (fix referrer). See which headers you should send. Log cookies