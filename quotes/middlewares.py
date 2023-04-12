from scrapy.downloadermiddlewares.defaultheaders import DefaultHeadersMiddleware
from random_header_generator.definitions import COUNTRIES as locales
from random_header_generator import HeaderGenerator
from scrapy.utils.python import without_none_values
from stem.control import EventType, Controller
from scrapy.exceptions import NotConfigured
from scrapy.http import Request, Response
from stem.response.events import Event
from stem import StreamStatus, Signal
from scrapy.crawler import Crawler
from functools import partial
from typing import Union
from quotes import URLDatabase
from scrapy import Spider
from time import sleep
from math import ceil

import random

class IPSwitchMiddleware():
    """ Middleware to change IP when requests start failing. """


    def __init__(self, port, password, IPSwitchCodes, proxyAddress, IPsettleTime):
        """Ininitialisation method """
        
        # TOR controller
        self.controller   = Controller.from_port(port = port)
        self.controller.authenticate(password = password)

        # Listener for NEWNYM signals
        streamListener    = partial(self._streamEvent, self.controller)
        self.controller.add_event_listener(streamListener, EventType.STREAM)

        self.IPsettleTime = IPsettleTime
        self.IPCodes      = IPSwitchCodes
        self.proxyAddress = proxyAddress
        self.targetIP     = None
        self.IPaddress    = None
        self.fingerprint  = None
        self.nickname     = None
        self.locale       = None
    
        return
    

    @classmethod
    def from_crawler(cls, crawler: Crawler):
        """ Instantiates class """

        if not crawler.settings.getbool("TOR_ENABLED"): raise NotConfigured
        
        return cls(port          = crawler.settings.get("TOR_CONTROL_PORT"), 
                   password      = crawler.settings.get("TOR_PASSWORD"),
                   IPSwitchCodes = crawler.settings.get("IP_CHANGE_CODES"), 
                   proxyAddress  = crawler.settings.get("PRIVOXY_PROXY_ADDRESS"), 
                   IPsettleTime  = crawler.settings.get("IP_SETTLE_TIME"), 
        )


    def _streamEvent(self, controller: Controller, event: Event) -> None:
        """ Extracts available information regarding the currently used exit node.
            Source: https://stem.torproject.org/tutorials/examples/exit_used.html
        """

        if event.status == StreamStatus.SUCCEEDED and event.circ_id:

            # Grab circuit and exit node
            circ             = controller.get_circuit(event.circ_id)
            exitFprint       = circ.path[-1][0]
            exit_relay       = controller.get_network_status(exitFprint)

            # Extract info
            self.targetIP    = event.target
            self.IPaddress   = f'{exit_relay.address}:{exit_relay.or_port}'
            self.fingerprint = exit_relay.fingerprint
            self.nickname    = exit_relay.nickname
            self.locale      = controller.get_info("ip-to-country/%s" % exit_relay.address, 'unknown')
    
        return


    def _renewConnection(self) -> None:
        """ Forces IP change on TOR. """
        
        wTime = ceil(self.controller.get_newnym_wait())
        sleep(wTime)                            # Wait until a new circuit can be built
        self.controller.signal(Signal.NEWNYM)   # Send signal to build a circuit        
        sleep(self.IPsettleTime)                # Wait until new IP settles in

        return
    
        
    def process_response(self, request: Request, response: Response, spider: Spider
        ) -> Union[Request, Response]:
        """ Renews IP depending on the response status """

        #if not 'robots' in response.url:
        #    if random.random() > 0.5:
        #        self._renewConnection()
        #        return request
        
        if response.status in self.IPCodes: # Force IP change
            self._renewConnection()
            return request

        return response
    

    def process_request(self, request: Request, spider: Spider) -> None:
        """ Sets the proxy and some related information for logging purposes """

        request.meta['proxy']       = self.proxyAddress
        request.meta['IPaddress']   = self.IPaddress
        request.meta['fingerprint'] = self.fingerprint
        request.meta['nickname']    = self.nickname
        request.meta['locale']      = self.locale 

        return


class HeadersMiddleware():
    """ Middleware to set request headers depending on current IP address. """

    def __init__(self, 
        user_agents = None, device = None, browser = None, httpVersion = None
        ) -> None:
        """ Initialisation method. """

        # Header generator object
        self.generator = partial(
            HeaderGenerator(user_agents), 
            device = device, browser = browser, httpVersion = httpVersion
            )
    
        # Initial values
        self.currentIP, self.headers = None, {}

        return


    @classmethod
    def from_crawler(cls, crawler):
        """ Instantiates class """
        
        if not crawler.settings.getbool("HEADER_GENERATOR_ENABLED"):
            # Crawl with default headers -> return the DefaultHeadersMiddleware

            headers = without_none_values(crawler.settings["DEFAULT_REQUEST_HEADERS"])
            return DefaultHeadersMiddleware(headers.items())
    
        else: # Crawl with randomly generated headers
            return cls(
                user_agents = crawler.settings.get("USER_AGENTS"),
                device      = crawler.settings.get("HEADER_DEVICE_TYPE"),
                browser     = crawler.settings.get("HEADER_BROWSER_NAME"), 
                httpVersion = crawler.settings.get("HEADER_HTTP_VERSION"), 
            )


    def process_request(self, request, spider) -> None:
        """ Updates request headers if needed. """

        if request.meta['IPaddress'] != self.currentIP: # Time to update headers
            
            # Update headers and stored IP
            self._update(locale = request.meta.get('locale', None))
            self.currentIP = request.meta.get('IPaddress', None)

        # Set request headers
        for key, value in self.headers.items():

            # Convert to bytes and replace (apart from referer if already set)
            bkey, bvalue = self._toBytes(key), self._toBytes(value)
            
            if (key not in ['Referer']) or (bkey not in request.headers.keys()):
                request.headers[bkey] = [bvalue]
        
        return
    

    def _update(self, locale: str) -> None:
        """ Updates headers """

        if locale in locales: 
            self.headers = self.generator(country = locale)
        else: 
            self.headers = self.generator(country = 'us')
        
        return


    @staticmethod
    def _toBytes(text:str, encoding: str = 'utf-8') -> bytearray:
        """ Strings to bytes converter. """
        return bytes(text, encoding)


class URLLoggerMiddleware():
    """ Middleware to log metadata for all succesful requests. """

    def __init__(self) -> None:
        """ Initialisation method """

        self.db   = URLDatabase
        self.null = 'N/A'
        
        return


    @classmethod
    def from_crawler(cls, crawler: Crawler):
        """ Instantiates class. """

        if not crawler.settings.getbool("URL_LOG_ENABLED"): raise NotConfigured
        return cls()
    

    def process_response(self, request: Request, response: Response, spider: Spider):
        """ Saves request metadata to an sqlite database """
        
        query = """
            INSERT OR IGNORE INTO 
            pages (url, status_code, date, fingerprint, IP_address, 
            server_name, locale, referer, user_agent, down_latency) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """
        
        task = (
            response.url,
            response.status,
            response.headers['date'].decode("utf-8"),
            request.meta.get('fingerprint', self.null),
            request.meta.get('IPaddress',   self.null),
            request.meta.get('nickname',    self.null),
            request.meta.get('locale',      self.null),
            request.headers.get('Referer', self.null).decode("utf-8"),
            request.headers.get('User-Agent', self.null).decode("utf-8"),
            request.meta.get('download_latency', self.null) # download latency
        )
        
        self.db.connect()
        self.db.cursor.execute(query, task)
        self.db.close()

        return response
    

    def process_request(self, request: Request, spider: Spider) -> None: return

