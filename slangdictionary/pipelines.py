from scrapy import Spider, Item
from scrapy.exceptions import DropItem

import sys
sys.path.append('../utils')
from utils.helpers import AbstractDBSavePipeline


class DefaultValuesPipeline():
    """ Sets default values to all fields of an item """

    def process_item(self, item: Item, spider: Spider) -> Item:
        """ Item processor """

        if not bool(item): raise DropItem()
        
        item.setdefault('word', '')
        item.setdefault('usage', {'hear': 0, 'no-hear': 0, 'no-use': 0, 'use': 0})
        item.setdefault('definitions', [''])
        item.setdefault('vulgarity', None)
        
        return item


class SavePipeline(AbstractDBSavePipeline):
    """ Saves item to the database """


    def process_item(self, item: Item, spider: Spider) -> Item:
        """ Save items in the database.
            This method is called for every item pipeline component
        """

        if not bool(item)  : raise DropItem()

        for d in item
        query = "INSERT OR IGNORE INTO authors (name, birthdate, birthplace, bio) VALUES (?, ?, ?, ?);"
        task  = (item['name'], item['birthdate'], item['birthplace'], item['bio'])
        
        self.db.execute(query, task)

        return item
    

