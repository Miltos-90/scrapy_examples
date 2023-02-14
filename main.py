# scrapy startproject abbreviation_scraper
# scrapy crawl quotes -o quotes.jsonl:jsonlines
# More examples and patterns: https://docs.scrapy.org/en/latest/intro/tutorial.html#intro-tutorial


# https://datawookie.dev/blog/2021/06/scrapy-rotating-tor-proxy/
# https://medium.com/hackernoon/web-scraping-tutorial-with-python-tips-and-tricks-db070e70e071


# ===============================================================
def clean():
    import os
    paths = ['./logger.log', './scrapy_quotes.db', './visited_urls.db']
    for filePath in paths:
        if os.path.isfile(filePath): 
            os.remove(filePath)

#clean()
# ===============================================================

"""
TODO:
Optimize insertQuote() inside databases.py to work with a single query.
"""

from scrapy.crawler import CrawlerProcess
from quotes.spiders.quotes_spider import QuotesSpider
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())
process.crawl(QuotesSpider)
#process.crawl(QuotesSpider2) ... Run multiple spiders here if needed
process.start() # the script will block here until all crawling jobs are finished