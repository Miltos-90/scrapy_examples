from headers import *
import random as rd

class GenericHeaderGenerator(HTTPHeaderGenerator):

    def __init__(self):

        self.browsers = list(UserAgent.data.keys())
        self.domains  = list(Referer.data.keys())

        return

    def __call__(self, browser:str = None, domain:str = None) -> dict:

        """ Generates realistic, randomly-chosen HTTP headers.

        Inputs: 
            * domain (list) can be either:
                * Empty: random selection among all
                * list containing one or more of: 
                    .com, .jsp, .edu, .org, .info, .net, .php3, .aspx, .biz, .uk,  .it,
                    .is,  .ua,  .cc,  .de,  .us,   .tv,  .eu, .ru, .cn, .jp, .nl, .be,  
                    .fr,  .ch,  .gr,  .se,   .dk,  .bg,  .cz, .hu, .lt, .pl, .ro, .sk, 
                    .si,  .br,  .pt,  .es,  .il,   .au,  .io,   .no,   .ir, .at

            * Browser (list) can be either
                * Empty: random selection among all
                * list containing one or more of: 
                    'chrome', 'firefox', 'safari', 'edge', 'opera'
        """

        if domain is None:  domain = rd.choice(self.domains) 
        else:               domain = rd.choice(domain) 

        if browser is None: browser = rd.choice(self.browsers)
        else:               browser = rd.choice(browser)

        userAgent = UserAgent(browser)

        headers = {
                "Sec-CH-UA-Mobile": UAMobile(userAgent),
                "User-Agent"      : userAgent,
                "Referer"         : Referer(domain), 
                "Accept"          : Accept(browser),
                "Accept-Language" : Language(domain, universal = ['en', 'en-GB', 'en-US']),
                "Accept-Encoding" : Encoder(addFactors = rd.random() >= 0.5),
                "Upgrade-insecure-requests": "1",
            }
            

        return headers

    """

        "sec-ch-ua": "\".Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"103\", \"Chromium\";v=\"103\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-site": "none",
        "sec-fetch-mod": "",
        "sec-fetch-user": "?1",
"""

if __name__ == "__main__":
    from user_agents import parse
    # https://www.whatismybrowser.com/detect/what-http-headers-is-my-browser-sending
    # https://apify.github.io/fingerprint-suite/docs/guides/header-generator/
    headers = GenericHeaderGenerator()
    
    for _ in range(10):

        h = headers()
        for k, v in h.items():
            print(f'{k}: {v}')

        agent = parse(h['User-Agent'])
        
        # Accessing user agent's browser attributes
        print(user_agent.browser  # returns Browser(family=u'Mobile Safari', version=(5, 1), version_string='5.1')
        print(user_agent.browser.family  # returns 'Mobile Safari'
        print(user_agent.browser.version  # returns (5, 1)
        print(user_agent.browser.version_string   # returns '5.1'

        # Accessing user agent's operating system properties
        print(user_agent.os  # returns OperatingSystem(family=u'iOS', version=(5, 1), version_string='5.1')
        user_agent.os.family  # returns 'iOS'
        user_agent.os.version  # returns (5, 1)
        user_agent.os.version_string  # returns '5.1'

        # Accessing user agent's device properties
        user_agent.device  # returns Device(family=u'iPhone', brand=u'Apple', model=u'iPhone')
        user_agent.device.family  # returns 'iPhone'
        user_agent.device.brand # returns 'Apple'
        user_agent.device.model # returns 'iPhone'

        # Viewing a pretty string version
        str(user_agent) # returns "iPhone / iOS 5.1 / Mobile Safari 5.1"