# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# by commenting out the setting in the settings.py file
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from quotes.utils import createConnection

class DefaultValuesPipeline(object):

    def __init__(self):
        return

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

    def process_item(self, item, spider):
        """ Save quotes in the database
            This method is called for every item pipeline component
        """
        
        connection = createConnection()
        cursor     = connection.cursor()

        # Save author
        query = "INSERT OR IGNORE INTO authors (name, birthdate, birthplace, bio) VALUES (?, ?, ?, ?)"
        task  = (item['author'], item['author_birthdate'], item['author_birth_loc'], item['author_bio'])
        cursor.execute(query, task)
        
        # Save quote
        authID = cursor.execute(
            "SELECT id FROM authors WHERE name = ?", (item['author'], )
            ).fetchone()[0]
        query  = "INSERT OR IGNORE INTO quotes (quote, tags, author_id) VALUES (?, ?, ?)"
        task   = (item['quote'], item['tag'], authID)
        cursor.execute(query, task)

        # Close connection
        connection.commit()
        cursor.close()
        connection.close()

        return item
