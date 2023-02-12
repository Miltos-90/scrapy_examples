# scrapy startproject abbreviation_scraper
# scrapy crawl quotes -o quotes.jsonl:jsonlines
# More examples and patterns: https://docs.scrapy.org/en/latest/intro/tutorial.html#intro-tutorial

# https://towardsdatascience.com/a-minimalist-end-to-end-scrapy-tutorial-part-i-11e350bcdec0
# https://github.com/harrywang/scrapy-tutorial/blob/master/tutorial/spiders/quotes_spider_v2.py
# https://datawookie.dev/blog/2021/06/scrapy-rotating-tor-proxy/
# https://medium.com/hackernoon/web-scraping-tutorial-with-python-tips-and-tricks-db070e70e071


"""
TODO
clean up / comment extension
check how not to be banned
"""

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
Downloadermiddleware:
record request from spider
record response
if response is an error (see here: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#client_error_responses)
retry based on error (in spider)
else get next link directly (in spider)

"""

        

from scrapy.crawler import CrawlerProcess
from quotes.spiders.quotes_spider import QuotesSpider
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())
process.crawl(QuotesSpider)
#process.crawl(QuotesSpider2) ... Run multiple spiders here if needed
process.start() # the script will block here until all crawling jobs are finished