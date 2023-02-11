from scrapy import signals
from scrapy.exceptions import NotConfigured
from datetime import datetime as dt


class ItemCounter:

    def __init__(self, item_count):
        self.item_count = item_count
        self.items_scraped = 0

    @classmethod
    def from_crawler(cls, crawler):

        # first check if the extension should be enabled and raise
        # NotConfigured otherwise
        if not crawler.settings.getbool('ITEM_COUNTER_ENABLED'):
            raise NotConfigured

        # get the number of items from settings
        item_count = crawler.settings.getint('ITEM_COUNTER_STEP', 1000)

        # instantiate the extension object
        ext = cls(item_count)

        # connect the extension object to signals
        crawler.signals.connect(ext.spider_opened,    signal = signals.spider_opened)
        crawler.signals.connect(ext.spider_closed,    signal = signals.spider_closed)
        crawler.signals.connect(ext.ItemPrint, signal = signals.item_scraped)

        # return the extension object
        return ext

    def spider_opened(self, spider):
        pass

    def spider_closed(self, spider):
        pass

    def ItemPrint(self, item, spider):

        self.items_scraped += 1
        if self.items_scraped % self.item_count == 0:
            
            print("Items scraped: {} ({})".format(self.items_scraped, self.now()))


    @staticmethod
    def now(): 
        return dt.now().strftime('%d-%m-%Y %H:%M:%S')
