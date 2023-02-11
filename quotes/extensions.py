from scrapy import signals
from scrapy.exceptions import NotConfigured
from datetime import datetime as dt
from quotes.databases import URLDatabase


class ProgressMonitor:

    def __init__(self, progressStep):

        self.progressStep  = progressStep  # Print every <progressStep> processed items
        self.itemsScraped  = 0             # Counter for the number of items processed
        self.lastPrintTime = None          # Time that the last progress message was printed
        self.startTime     = None          # Time the crawler started 
        self.db            = URLDatabase() 

    @classmethod
    def from_crawler(cls, crawler):

        # first check if the extension should be enabled 
        if not crawler.settings.getbool('PROGRESS_MONITOR_ENABLED'):
            raise NotConfigured

        # instantiate the extension object
        step = crawler.settings.getint('PROGRESS_MONITOR_STEP', 1000)
        ext  = cls(progressStep = step)

        # connect the extension object to signals
        crawler.signals.connect(ext.spiderOpened, signal = signals.spider_opened)
        crawler.signals.connect(ext.spiderClosed, signal = signals.spider_closed)
        crawler.signals.connect(ext.printProgress, signal = signals.item_scraped)

        # return the extension object
        return ext

    def spiderOpened(self, spider):

        self._updateTimer()
        self.startTime = self.lastPrintTime
        print("Crawler started at {}".format(self.lastPrintTime.strftime('%d-%m-%Y %H:%M:%S')))
        return 

    def spiderClosed(self, spider):

        self._updateTimer()
        print("Crawler stopped at {}".format(self.lastPrintTime.strftime('%d-%m-%Y %H:%M:%S')))
        return 

    def printProgress(self, item, spider):

        self._updateCounter()

        if self._makeReport():
            
            # Report progress
            msg = "Items scraped: {}. Last URL processed: {}. Crawler rate (items/sec): {}. Reported on: {})"\
            .format(
                self.itemsScraped, 
                self._lastUrl(),
                self._scrapeRate(),
                dt.now().strftime('%d-%m-%Y %H:%M:%S')
                )
            print(msg)

        self._updateTimer()

        return

    def _makeReport(self):  return self.itemsScraped % self.progressStep == 0
    def _updateTimer(self): self.lastPrintTime = dt.now()
    def _updateCounter(self): self.itemsScraped += 1

    def _lastUrl(self):
        self.db.connect()
        lastPage = self.db.last()
        self.db.close()

        return lastPage

    def _scrapeRate(self):
        elapsedTime = (dt.now() - self.startTime).total_seconds()
        return self.itemsScraped / elapsedTime


