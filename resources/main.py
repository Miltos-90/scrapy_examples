# TODO:
# Sec-CH-UA finish
# Randomly select user-agend and domain. Then infer all the rest.
# Find list of user agents!

# Useful info
# https://www.whatismybrowser.com/detect/what-http-headers-is-my-browser-sending
# https://apify.github.io/fingerprint-suite/docs/guides/header-generator/

# User agent generator
# https://github.com/iamdual/ua-generator

# User agent lists
# https://gist.github.com/pzb/b4b6f57144aea7827ae4
# https://pastebin.com/csVFA72Y
# https://www.useragentstring.com/pages/All/
# https://developers.whatismybrowser.com/useragents/database/
# https://www.whatismybrowser.com/guides/the-latest-user-agent/chrome
# https://github.com/tamimibrahim17/List-of-user-agents
# https://github.com/N0taN3rd/userAgentLists/tree/master/uagents/csv
    

from headers import *
import random as rd
import re

class GenericHeaderGenerator(HTTPHeaderGenerator):

    def __init__(self):

        self.UserAgent  = HTTPHeaderGenerator('./data/userAgents.json')
        self.Referer    = HTTPHeaderGenerator('./data/referers.json')
        self.Encoder    = AcceptEncoding('./data/acceptEncoding.json')
        self.Language   = AcceptLanguage('./data/languages.json')
        self.Accept     = Accept('./data/accept.json')
        self.browsers   = list(self.UserAgent.data.keys())
        self.domains    = list(self.Referer.data.keys())

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

        userAgent = self.UserAgent(browser)

        headers = {
            "User-Agent"      : userAgent,
            "Referer"         : self.Referer(domain), 
            "Accept"          : self.Accept(browser),
            "Accept-Language" : self.Language(domain, universal = ['en', 'en-GB', 'en-US'], qFactors = True),
            "Accept-Encoding" : self.Encoder(qFactors = rd.random() >= 0.5),
            "DNT"             : "1",
            "Upgrade-insecure-requests": "1",
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Sec-CH-Prefers-Reduced-Motion" : rd.choice(["no-preference", "reduce"])
        }
        

        return headers


class DetectMobileBrowser(object):
    """ Checks if a user-agent string comes from the browser of a mobile device.
        Modified from Matt Sullivan http://sullerton.com/2011/03/django-mobile-browser-detection-middleware/,
        as provided in: http://detectmobilebrowsers.com/
    """

    reg_b = re.compile(r"(android|bb\\d+|meego).+mobile|avantgo|bada\\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\\.(browser|link)|vodafone|wap|windows ce|xda|xiino", re.I|re.M)
    reg_v = re.compile(r"1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\\-(n|u)|c55\\/|capi|ccwa|cdm\\-|cell|chtm|cldc|cmd\\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\\-s|devi|dica|dmob|do(c|p)o|ds(12|\\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\\-|_)|g1 u|g560|gene|gf\\-5|g\\-mo|go(\\.w|od)|gr(ad|un)|haie|hcit|hd\\-(m|p|t)|hei\\-|hi(pt|ta)|hp( i|ip)|hs\\-c|ht(c(\\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\\-(20|go|ma)|i230|iac( |\\-|\\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\\/)|klon|kpt |kwc\\-|kyo(c|k)|le(no|xi)|lg( g|\\/(k|l|u)|50|54|\\-[a-w])|libw|lynx|m1\\-w|m3ga|m50\\/|ma(te|ui|xo)|mc(01|21|ca)|m\\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\\-2|po(ck|rt|se)|prox|psio|pt\\-g|qa\\-a|qc(07|12|21|32|60|\\-[2-7]|i\\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\\-|oo|p\\-)|sdk\\/|se(c(\\-|0|1)|47|mc|nd|ri)|sgh\\-|shar|sie(\\-|m)|sk\\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\\-|v\\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\\-|tdg\\-|tel(i|m)|tim\\-|t\\-mo|to(pl|sh)|ts(70|m\\-|m3|m5)|tx\\-9|up(\\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\\-|your|zeto|zte\\-", re.I|re.M)


    def __call__(self, s):
                
        if self.reg_b.search(s) or self.reg_v.search(s[0:4]):
            return True
        else:
            return False


if __name__ == "__main__":
    
    from uaparser import UAParser
    
    headers = GenericHeaderGenerator()
    
    for _ in range(1):

        h = headers()
        #for k, v in h.items():
        #    print(f'{k}: {v}')

        """ 
        User Agent Hints

        No. Available   Field                           
        --  ---------   ----------------------------
        1   No          Sec-CH-UA
        2   Yes         Sec-CH-UA-Arch
        3   No          Sec-CH-UA-Bitness
        4   No          Sec-CH-UA-Full-Version-List
        5   Yes         Sec-CH-UA-Mobile
        6   Yes         Sec-CH-UA-Model
        7   Yes         Sec-CH-UA-Platform
        8   Yes         Sec-CH-UA-Platform-Version
        9   Yes         Sec-Fetch-Site
        10  Yes         Sec-Fetch-Mode
        11  Yes         Sec-Fetch-User
        12  Yes         Sec-Fetch-Dest
        13  Yes         Sec-CH-Prefers-Reduced-Motion 
        ---------------------------------------------
        For more info see: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers, https://github.com/WICG/ua-client-hints

        """

        s = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        s = "Samsung SM-T820 / Android 9 / Chrome Mobile WebView 85.0.4183"
        s = "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.49"
        s = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41"

        gg = UAParser.parse(s)
        isMobile = DetectMobileBrowser()

        for k, v in gg.items():
            print(f'{k}: {v}')
        print()

        _format         = lambda x: f'\"{x}\"' if x is not None else '\"\"'
        mobile          = f"?{int(isMobile(s))}"
        platform        = _format(gg['os']['name'])
        platformVersion = _format(gg['os']['version'])
        model           = _format(gg['device']['model'])
        arch            = _format(gg['cpu']['architecture'])

        print('2', 'Sec-CH-UA-Arch', ':', arch)
        print('5', 'Sec-CH-UA-Mobile', ':', mobile)
        print('6', 'Sec-CH-UA-Model', ':', model)
        print('7', 'Sec-CH-UA-Platform', ':', platform)
        print('8', 'Sec-CH-UA-Platform-Version', ':', platformVersion)

        brand   = _format(gg['browser']['name'])
        version = _format(gg['browser']['major'])

        print(brand, version)

        #Not A(Brand

        #rd.choi
        #print()

        #    ["edge", "Microsoft Edge"],
        #    ["opera", "Opera"],
        #    ["firefox", "Mozilla Firefox"],
        #    ["chrome", "Google Chrome"],
        #    ["safari", "Apple Safari"],
        #    ["msie", "Internet Explorer"]
        

    """
    Sec-CH-UA: "(Not(A:Brand";v="8", "Chromium";v="98"    
    Sec-CH-UA: " Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"
    Sec-CH-UA: " Not A;Brand";v="99", "Chromium";v="96", "Microsoft Edge";v="96"
    Sec-CH-UA: "Opera";v="81", " Not;A Brand";v="99", "Chromium";v="95"
    """

        
        

        
        