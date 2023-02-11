# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# by commenting out the setting in the settings.py file
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from quotes.databases import QuoteDatabase, URLDatabase
from scrapy import Spider


class UrlManagementPipeline(object):
    """ Insers visited URLs to the database """

    def __init__(self):
        self.db = URLDatabase()

    def process_item(self, item, spider):

        self.db.connect()
        self.db.insert(item['url'])
        self.db.close()
        return item


class DefaultValuesPipeline(object):
    """ Sets default values to all fields """

    def process_item(self, item, spider: Spider):
        """ Save quotes in the database
            This method is called for every item pipeline component
        """

        # Set default values
        item.setdefault('quote',            'not found')
        item.setdefault('author',           'not found')
        item.setdefault('tag',              'not found')
        item.setdefault('author_bio',       'not found')
        item.setdefault('author_birthdate', 'not found')
        item.setdefault('author_birth_loc', 'not found')
        
        return item


class SaveQuotesPipeline(object):
    """ Inserts quotes to the database """

    def __init__(self):
        self.db = QuoteDatabase()

        return

    def process_item(self, item, spider: Spider):
        """ Save quotes in the database
            This method is called for every item pipeline component
        """
        
        self.db.connect()
        self.db.insertAuthor(item)
        self.db.insertQuote(item)
        self.db.close()

        return item

