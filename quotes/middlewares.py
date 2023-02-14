"""
Define here the models for your spider and downloader middleware.

=====================================================================================
Spider middleware documentation in:
https://docs.scrapy.org/en/latest/topics/spider-middleware.html

Spider middlewares are specific hooks that sit between the Engine and the 
Spiders and are able to process spider input (responses) and output (items and requests).

Use a Spider middleware if you need to do the following:
* post-process output of spider callbacks - change/add/remove requests or items;
* post-process start_requests;
* handle spider exceptions;
* call errback instead of callback for some of the requests based on response content.

=====================================================================================
Downloader middleware documentation in: 
https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#topics-downloader-middleware

Downloader middlewares are specific hooks that sit between the Engine and the Downloader and 
process requests when they pass from the Engine to the Downloader, and responses that pass from Downloader to the Engine.

Use a Downloader middleware if you need to do one of the following:
* process a request just before it is sent to the Downloader (i.e. right before Scrapy sends the request to the website);
* change received response before passing it to a spider;
* send a new Request instead of passing received response to a spider;
* pass response to a spider without fetching a web page;
* silently drop some requests.
""" 

from scrapy import signals

class QuotesSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    def __init__(self): 

        return


    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        """ Called with the results returned from the Spider, after
            it has processed the response.
        """

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class QuotesDownloaderMiddleware(object):

    def __init__(self): 

        return
    
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s


    def process_request(self, request, spider):
        """ Called for each request that goes through the downloader
            middleware (i.e. right before Scrapy sends the request to the website).
        """ 

        return


    def process_response(self, request, response, spider):
        """ Called with the response returned from the downloader 
            (i.e. right before it is being passed to the spider).
        """

        return response

    def process_exception(self, request, exception, spider):
        """ Called when a download handler or a process_request()
            (from other downloader middleware) raises an exception.
        """
        
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
