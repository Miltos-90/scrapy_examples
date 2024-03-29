from random_header_generator.definitions import COUNTRIES
from random_header_generator import HeaderGenerator
from stem.control import EventType, Controller
from scrapy.exceptions import NotConfigured
from scrapy.http import Request, Response
from stem.response.events import Event
from stem import StreamStatus, Signal
from scrapy import Spider, signals
from scrapy.crawler import Crawler
from functools import partial
from .helpers import Database
from typing import Union
from . import  constants
from time import sleep
from math import ceil
import requests


class IPSwitchMiddleware():
    """ Middleware to change IP when requests start failing. """

    def __init__(self, 
        port: str, password: str, IPSwitchCodes: list[int], proxyAddress: str, IPsettleTime: int):
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
        self.IPaddress    = None
        self.fingerprint  = None
        self.nickname     = None
        self.locale       = None

        # Trigger a one-time stream event to gather the initial exit node's info
        requests.request(url = 'https://www.icanhazip.com', method = 'GET').text.strip('\n')
    
        return
    

    @classmethod
    def from_crawler(cls, crawler: Crawler):
        """ Instantiates class """

        if not crawler.settings.getbool("TOR_ENABLED", default = False): 
            raise NotConfigured
        
        return cls(
            port          = crawler.settings.get("TOR_CONTROL_PORT",  default = constants.PORT),
            password      = crawler.settings.get("TOR_PASSWORD",      default = constants.PASSWORD),
            proxyAddress  = crawler.settings.get("TOR_PROXY_ADDRESS", default = constants.PROXY),
            IPSwitchCodes = crawler.settings.get("IP_CHANGE_CODES"),
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
            self.IPaddress   = f'{exit_relay.address}:{exit_relay.or_port}'
            self.fingerprint = exit_relay.fingerprint
            self.nickname    = exit_relay.nickname
            self.locale      = controller.get_info("ip-to-country/%s" % exit_relay.address, 'unknown')
    
        return


    def _renewConnection(self) -> None:
        """ Forces IP change on TOR. """
        
        wTime = ceil(self.controller.get_newnym_wait())
        sleep(wTime)
        self.controller.signal(Signal.NEWNYM)   
        sleep(self.IPsettleTime)

        return
    
        
    def process_response(self, 
        request: Request, response: Response, spider: Spider) -> Union[Request, Response]:
        """ Renews IP depending on the response status """
        
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
        self.referer = self._toBytes('Referer')

        return


    @classmethod
    def from_crawler(cls, crawler: Crawler):
        """ Instantiates class """
        
        if not crawler.settings.getbool("HEADER_GENERATOR_ENABLED", default = False): 
            raise NotConfigured
    
        return cls(
            user_agents = crawler.settings.get("USER_AGENTS"),
            device      = crawler.settings.get("HEADER_DEVICE_TYPE"),
            browser     = crawler.settings.get("HEADER_BROWSER_NAME"), 
            httpVersion = crawler.settings.get("HEADER_HTTP_VERSION")
            )
    

    def process_request(self, request: Request, spider: Spider) -> None:
        """ Updates request headers if needed. """

        if request.meta['IPaddress'] != self.currentIP: # Time to update headers
            
            # Update headers and stored IP
            self._update(locale = request.meta.get('locale', None))
            self.currentIP = request.meta.get('IPaddress', None)

        # Set request headers
        for key, value in self.headers.items():
            
            # Get referer set by the spider middlewares if exists
            if key == self.referer: 
                value = request.headers.pop(key, self.headers[key])
            
            request.headers[key] = value
        
        return
    

    def _update(self, locale: str) -> None:
        """ Updates headers """

        if locale not in COUNTRIES: locale = 'us'

        self.headers = {
            self._toBytes(k): [self._toBytes(v)] 
            for k, v in self.generator(country = locale).items()
            }
        
        return


    @staticmethod
    def _toBytes(text: str, encoding: str = 'utf-8') -> bytearray:
        """ Strings to bytes converter. """
        return bytes(text, encoding)


class URLLoggerMiddleware():
    """ Middleware to log metadata for all succesful requests. """

    # Default settings values
    DB_FILE   = "./url_logger.db"

    DB_SCHEMA = """
        -- scraped pages schema
        CREATE TABLE IF NOT EXISTS pages (
            id           INTEGER PRIMARY KEY,
            url          TEXT    NOT NULL,
            date         TEXT    NOT NULL,
            status_code  INTEGER NOT NULL,
            fingerprint  TEXT,
            IP_address   TEXT,
            server_name  TEXT,
            locale       TEXT,
            referer      TEXT,
            user_agent   TEXT,
            down_latency REAL
        ) STRICT;
    """

    DB_PRAGMA = """
        PRAGMA foreign_keys=OFF;
        PRAGMA journal_mode=WAL;
        PRAGMA synchronous=FULL;
    """

    def __init__(self, filePath: str, pragma: str, schema: str) -> None:
        """ Initialisation method """

        self.null = 'N/A'
        self.db   = Database(filePath, schema, pragma)
        
        return


    @classmethod
    def from_crawler(cls, crawler: Crawler):
        """ Instantiates class. """

        if not crawler.settings.getbool("URL_LOG_ENABLED"): raise NotConfigured

        # Make class
        c = cls(
            filePath = crawler.settings.get("URL_LOG_DB",    default = URLLoggerMiddleware.DB_FILE),
            pragma   = crawler.settings.get("URL_DB_PRAGMA", default = URLLoggerMiddleware.DB_PRAGMA),
            schema   = crawler.settings.get("URL_DB_SCHEMA", default = URLLoggerMiddleware.DB_SCHEMA)
        )

        # Connect signals
        crawler.signals.connect(c.db.spiderOpened, signal = signals.spider_opened)
        crawler.signals.connect(c.db.spiderClosed, signal = signals.spider_closed)

        return c
    

    def process_request(self, request: Request, spider: Spider) -> None: return
    

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
            request.headers.get('Referer',  self.null).decode("utf-8"),
            request.headers.get('User-Agent', self.null).decode("utf-8"),
            request.meta.get('download_latency', self.null) # download latency
        )
        
        self.db.execute(query, task)

        return response
    
    