
from scrapy.downloadermiddlewares.defaultheaders import DefaultHeadersMiddleware
from random_header_generator import HeaderGenerator 
from stem.control import EventType, Controller
from scrapy.exceptions import NotConfigured
from scrapy.http import Request, Response
from stem.response.events import Event
from stem import StreamStatus, Signal
from scrapy.crawler import Crawler
from functools import partial
from quotes import URLDatabase
from scrapy import Spider
from time import sleep
from math import ceil

import random

class TorHandlerMiddleware():


    def __init__(self, port, password, IPSwitchCodes, proxyAddress, IPsettleTime):
        """Ininitialisation method """
                
        self.controller   = Controller.from_port(port = port)
        self.controller.authenticate(password = password)

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
    
        
    def process_response(self, request: Request, response: Response, spider: Spider):
        """ Get a new identity depending on the response """

        #if not 'robots' in response.url:
        #    if random.random() > 0.75:# if response.status in self.IPCodes: # Force IP change
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


class URLLoggerMiddleware():

    def __init__(self):
        """ Initialisation method """
        self.db = URLDatabase


    @classmethod
    def from_crawler(cls, crawler: Crawler):

        if not crawler.settings.getbool("URL_LOG_ENABLED"): raise NotConfigured
        return cls()
    

    def process_response(self, request: Request, response: Response, spider: Spider):
        
        query = """
            INSERT OR IGNORE INTO 
            pages (url, status_code, date, fingerprint, IP_address, server_name, locale, down_latency) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """

        task = (
            response.url,                               # url
            response.status,                            # status_code
            response.headers['date'].decode("utf-8"),   # date
            request.meta['fingerprint'],       # fingerprint
            request.meta['IPaddress'],         # IP_address
            request.meta['nickname'],          # server_name
            request.meta['locale'],            # locale
            request.meta['download_latency']   # download latency
        )
        
        self.db.connect()
        self.db.cursor.execute(query, task)
        self.db.close()

        return response
    

    def process_request(self, request: Request, spider: Spider) -> None: return



class HeadersMiddleware(DefaultHeadersMiddleware):

    generator = HeaderGenerator()

    def process_request(self, request, spider):
        # TODO
        print(request.meta)
        #for k, v in self._headers:
        #    request.headers.setdefault(k, v)