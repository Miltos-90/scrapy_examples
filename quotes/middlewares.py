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

import functools
from stem import Signal
from stem.control import Controller
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from scrapy.downloadermiddlewares.defaultheaders import DefaultHeadersMiddleware
from scrapy.utils.project import get_project_settings
from stem import StreamStatus
from stem.control import EventType, Controller
from math import ceil
from time import sleep
from random_header_generator import HeaderGenerator 

SETTINGS = get_project_settings()


class TorHandlerMiddleware(HttpProxyMiddleware):


    def __init__(self, *args) -> None:
        """Ininitialisation method """
        
        super().__init__(args)
        
        self.controller = Controller.from_port(port = SETTINGS['TOR_CONTROL_PORT'])
        self.controller.authenticate(password = SETTINGS['TOR_PASSWORD'])

        streamListener  = functools.partial(self.streamEvent, self.controller)
        self.controller.add_event_listener(streamListener, EventType.STREAM)
        
        self.IPsettleTime = 2 # Wait time for the new IP to "settle in"
        self.renewConnection()
    
        return 
    

    def streamEvent(self, controller, event):
        """ Extracts available information regarding the currently used exit node.
            Source: https://stem.torproject.org/tutorials/examples/exit_used.html
        """

        if event.status == StreamStatus.SUCCEEDED and event.circ_id:

            # Grab circuit
            circ = controller.get_circuit(event.circ_id)

            # Get exit node
            exitFprint = circ.path[-1][0]
            exit_relay  = controller.get_network_status(exitFprint)

            # Extract info
            self.targetIP    = event.target
            self.IPaddress   = f'{exit_relay.address}:{exit_relay.or_port}'
            self.fingerprint =  exit_relay.fingerprint
            self.nickname    = exit_relay.nickname
            self.locale      = controller.get_info("ip-to-country/%s" % exit_relay.address, 'unknown')


            with open('./output.txt', mode = 'a', encoding = 'utf-8') as f:
                f.write("\n")
                f.write("====================================================\n")
                f.write("  Exit relay for our connection to %s\n" % (event.target))
                f.write("  address: %s:%i\n" % (exit_relay.address, exit_relay.or_port))
                f.write("  fingerprint: %s\n" % exit_relay.fingerprint)
                f.write("  nickname: %s\n" % exit_relay.nickname)
                f.write("  locale: %s\n" % controller.get_info("ip-to-country/%s" % exit_relay.address, 'unknown'))
                f.write("====================================================")
                f.write("\n")



    def renewConnection(self):
        """ Forces IP change on TOR. """
        
        # Wait until a new circuit can be built
        waitTime = ceil(self.controller.get_newnym_wait())
        sleep(waitTime)

        # Send signal to build a circuit
        self.controller.signal(Signal.NEWNYM)
        
         # Wait until new IP settles in
        sleep(self.IPsettleTime)
    
        
    def process_response(self, request, response, spider):
        """ Get a new identity depending on the response """

        if response.status in SETTINGS['RETRY_HTTP_CODES']: 
            # Force IP change before retrying in the RetryMiddleware
            self.renewConnection()

        return response

    def process_request(self, request, spider):
        """ Sets the proxy and some related information for logging purposes """
        request.meta['proxy']       = SETTINGS['PRIVOXY_PROXY_ADDRESS']
        
        #print(self.IPaddress)
        #request.meta['IPaddress']   = self.IPaddress
        #request.meta['fingerprint'] = self.fingerprint
        #request.meta['nickname']    = self.nickname
        #request.meta['locale']      = self.locale 

        return


class HeadersMiddleware(DefaultHeadersMiddleware):

    generator = HeaderGenerator()

    def process_request(self, request, spider):
        # TODO
        print(request.meta)
        #for k, v in self._headers:
        #    request.headers.setdefault(k, v)