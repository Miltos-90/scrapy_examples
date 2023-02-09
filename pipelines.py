# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# by commenting out the setting in the settings.py file
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html



from scrapy.utils.project import get_project_settings
from datetime import datetime
import sqlite3
from models import createConnection

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
        item.setdefault('author_birthdate', datetime(1,1,1))
        item.setdefault('author_birth_loc', 'not found')
        
        return item


class SaveQuotesPipeline(object):

    def __init__(self):
        """
        Initializes any connections as required
        """
        self.dbFile = get_project_settings().get("DB_FILE")
        
        return


    def process_item(self, item, spider):
        """ Save quotes in the database
            This method is called for every item pipeline component
        """
        
        connection = createConnection(self.dbFile)
        cursor     = connection.cursor()

        # Close connection
        connection.commit()
        cursor.close()
        connection.close()

        return item
