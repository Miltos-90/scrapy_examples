from ua_generator.generators import UserAgentGenerator as UAGenerator
from user_agent_parser import UAParser

if __name__ == '__main__':

    #device  = ('desktop', 'mobile')
    #os      = ('windows', 'macos', 'ios', 'linux', 'android')
    #browser = ('chrome', 'edge', 'firefox', 'safari')
    pg = UAGenerator()
    for _ in range(250):
        p = pg()
        #print(p)

uaStrings = [
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.2 (KHTML, like Gecko) Ubuntu/11.10 Chromium/15.0.874.106 Chrome/15.0.874.106 Safari/535.2',
    'Mozilla/5.0 (compatible; Konqueror/4.1; OpenBSD) KHTML/4.1.4 (like Gecko)',
    'Mozilla/5.0 (PlayBook; U; RIM Tablet OS 1.0.0; en-US) AppleWebKit/534.11 (KHTML, like Gecko) Version/7.1.0.7 Safari/534.11'
    ]

for s in uaStrings:

    result = UAParser(s)

    print(s)
    print(result.browser)  # {'name': 'Chromium', 'version': '15.0.874.106', 'major': '15'}
    print(result.device)  # {'vendor': None, 'model': None, 'type': None}
    print(result.os)  # {'name': 'Ubuntu', 'version': '11.10'}
    print(result.os['version'])  # '11.10'
    print(result.engine['name'])  # 'WebKit'
    print(result.cpu['architecture'])  # 'amd64'
    print()