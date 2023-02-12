from scrapy import signals
from scrapy.exceptions import NotConfigured
from datetime import datetime as dt
from quotes.databases import URLDatabase

from scrapy import Spider

spider = Spider


class ProgressMonitor:


    def __init__(self, numSteps):

        self.numSteps  = numSteps  # Print every <numSteps> processed items
        self.itemCount = 0             # Counter for the number of items processed
        self.startTime = None          # Time the crawler started 
        self.tFormat  = '%d-%m-%Y %H:%M:%S'
        self.db        = URLDatabase() # Database with URLs


    @classmethod
    def from_crawler(cls, crawler):
        """ Instantiate the extension and connect signals """

        # Check if the extension should be enabled 
        if not crawler.settings.getbool('PROGRESS_MONITOR_ENABLED'):
            raise NotConfigured

        # instantiate the extension object
        step = crawler.settings.getint('PROGRESS_MONITOR_STEP', 1000)
        ext  = cls(numSteps = step)

        # Map extension object to signals
        crawler.signals.connect(ext.spiderOpened, signal = signals.spider_opened)
        crawler.signals.connect(ext.spiderClosed, signal = signals.spider_closed)
        crawler.signals.connect(ext.itemScraped,  signal = signals.item_scraped)

        return ext


    def spiderOpened(self, spider):
        """ Execute on spider_opened signal """

        self.startTime = dt.now()
        print("{} | Crawler started.".format(self._now()))
        return 


    def spiderClosed(self, spider):
        """ Execute on spider_closed signals """

        print("\n{} | Crawler stopped.".format(self._now()))
        return 


    def itemScraped(self, item, spider):
        """ Execute on item_scraped signals """

        self.itemCount += 1

        if self._makeReport(): 

            rate = self._scrapeRate()
            url  = self._lastUrl()
            time = self._now()
            msg  = "{} | Items scraped: {} ({:.2f} items/sec) | Last visited: {}"\
                    .format(time, self.itemCount, rate, url)
            
            print(msg, end = '\r')

        return


    def _now(self) -> str: 
        """ Get current time formatted """
        
        return dt.now().strftime(self.tFormat)
    

    def _makeReport(self) -> bool:
        """ Checks if a progress message should be printed.
            (1 = yes / 0 = no) 
        """
        
        return self.itemCount % self.numSteps == 0
    

    def _lastUrl(self):
        """ Get last visited URL """

        self.db.connect()
        lastPage = self.db.last()
        self.db.close()

        return lastPage


    def _scrapeRate(self):
        """ Compute scraping speed [items/sec] """

        elapsedTime = (dt.now() - self.startTime).total_seconds()
        return self.itemCount / elapsedTime


