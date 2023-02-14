# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# by commenting out the setting in the settings.py file
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from quotes import QuotesDatabase


class DefaultValuesPipeline(object):
    """ Sets default values to all fields """

    def process_item(self, item, spider):
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

    def process_item(self, item, spider):
        """ Save quotes in the database
            This method is called for every item pipeline component
        """
        
        QuotesDatabase.connect()

        # Insert new author
        query = "INSERT OR IGNORE INTO authors (name, birthdate, birthplace, bio) VALUES (?, ?, ?, ?);"
        task  = (item['author'], item['author_birthdate'], item['author_birth_loc'], item['author_bio'])
        QuotesDatabase.cursor.execute(query, task)

        # Insert new quote
        query = """
            INSERT OR IGNORE INTO quotes (quote, tags, author_id)
            SELECT ?, ?, (SELECT id FROM authors WHERE name = ?);
        """
        task = (item['quote'], item['tag'], item['author'])
        QuotesDatabase.cursor.execute(query, task)
        
        QuotesDatabase.close()

        return item

