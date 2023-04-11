from quotes import QuotesDatabase
from scrapy import Spider, Item
from scrapy.exceptions import DropItem


def isAuthor(item) -> bool: return bool(item) and "name" in item.keys()
def isQuote(item)  -> bool: return bool(item) and "quote" in item.keys()

class DefaultValuesPipeline():
    """ Sets default values to all fields of an item """

    def process_item(self, item: Item, spider: Spider) -> Item:
        """ Save quotes in the database
            This method is called for every item pipeline component
        """

        if isAuthor(item):
            return DefaultAuthorValuesPipeline.process_item(item)

        elif isQuote(item):
            return DefaultQuoteValuesPipeline.process_item(item)
        else:
            raise DropItem()

class DefaultQuoteValuesPipeline():
    """ Sets default values to all fields """

    @staticmethod
    def process_item(item: Item) -> Item:
        """ Save quotes in the database
            This method is called for every item pipeline component
        """

        # Set default values
        item.setdefault('quote',    'not found')
        item.setdefault('author',   'not found')
        item.setdefault('keywords', 'not found')
        
        return item
    

class DefaultAuthorValuesPipeline(object):
    """ Sets default values to all fields """

    @staticmethod
    def process_item(item: Item) -> Item:
        """ Save quotes in the database
            This method is called for every item pipeline component
        """

        # Set default values
        item.setdefault('name',       'not found')
        item.setdefault('bio',        'not found')
        item.setdefault('birthdate',  'not found')
        item.setdefault('birthplace', 'not found')
        
        return item


class SavePipeline():
    """ Saves item to the database """

    def process_item(self, item: Item, spider: Spider) -> Item:
        """ Save quotes in the database
            This method is called for every item pipeline component
        """

        if isAuthor(item):
            return SaveAuthorPipeline.process_item(item)

        elif isQuote(item):
            return SaveQuotePipeline.process_item(item)


class SaveQuotePipeline():
    """ Inserts quotes to the database """

    @staticmethod
    def process_item(item: Item) -> Item:
        """ Save quotes in the database
            This method is called for every item pipeline component
        """
        
        QuotesDatabase.connect()
        
        query = "INSERT OR IGNORE INTO quotes (quote, keywords, author) VALUES (?, ?, ?);"
        task  = (item['quote'], item['keywords'], item['author'])
        QuotesDatabase.cursor.execute(query, task)
        
        QuotesDatabase.close()

        return item
    

class SaveAuthorPipeline(object):
    """ Inserts quotes to the database """

    @staticmethod
    def process_item(item: Item) -> Item:
        """ Save authors in the database
            This method is called for every item pipeline component
        """
        
        QuotesDatabase.connect()
        
        query = "INSERT OR IGNORE INTO authors (name, birthdate, birthplace, bio) VALUES (?, ?, ?, ?);"
        task  = (item['name'], item['birthdate'], item['birthplace'], item['bio'])
        QuotesDatabase.cursor.execute(query, task)

        QuotesDatabase.close()

        return item

