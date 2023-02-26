""" TESTING VARIOUS STUFF: https://whatmyuseragent.com/platforms

"""

import re
from parser_utils import str_mapper, lowerize, trim
from parser_utils import EMPTY
from dataclasses import dataclass
from typing import Callable

from test import test


OLD_SAFARI_MAP = {
    '1.0': '/8',
    '1.2': '/1',
    '1.3': '/3',
    '2.0': '/412',
    '2.0.2': '/416',
    '2.0.3': '/417',
    '2.0.4': '/419',
    '?': '/'
}


WINDOWS_VERSION_MAP = {
    'ME': '4.90',
    'NT 3.11': 'NT3.51',
    'NT 4.0': 'NT4.0',
    '2000': 'NT 5.0',
    'XP': ['NT 5.1', 'NT 5.2'],
    'Vista': 'NT 6.0',
    '7': 'NT 6.1',
    '8': 'NT 6.2',
    '8.1': 'NT 6.3',
    '10': ['NT 6.4', 'NT 10.0'],
    'RT': 'ARM'
}





@dataclass
class Mapper(object):
    """ Regex mapper. 
        Maps a property <key> of a Regex object to a value <value>
    """

    key   : str      = None
    value : str      = None
    func  : Callable = None
    re    : str      = None


@dataclass
class Regex():
    expr    : str   = None
    mappers : tuple = ()


def RegexpMapper(mapper: Mapper, match) -> tuple:

    if mapper.value is None and \
           mapper.func is None and \
           mapper.re is None:
           # No properties are specified. Replace key with the match found
           outValue = match

    elif mapper.value is not None:
            # Assign given value and ignore match
            outValue = mapper.value
            
    elif mapper.func is not None:
            # Assign value from specified function
            outValue = mapper.func(match)

    elif mapper.re is not None:
            # Sanitize match using given regex
            outValue = re.sub(mapper.re, mapper.value.replace('$', '\\'), match) if match else None
            
    return mapper.key, outValue

        



wtf = [
    Regex(
        expr = r'\b(?:crmo|crios)\/([\w\.]+)',
        mappers = (
            Mapper(key = 'version'),
            Mapper(key = 'name', value = 'Chrome')
            )
        ),
    Regex(
        expr = r'(avast|avg)\/([\w\.]+)',
        mappers = (
            Mapper(key = 'version'),
            Mapper(
                key   = 'name', 
                value = '$1 Secure ' + 'Browser',
                re = r'(.+)'
                )
            )
        )
]

for entry in wtf:
    entry.expr = re.compile( entry.expr, re.IGNORECASE)

ua = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36 Avast/99.0.15283.83'



# loop through all regexes maps
for entry in wtf:
        
    # try matching uastring with regexes
    matches = entry.expr.search(ua)
        
    if matches: break
    
    if matches:
        
        for mapper in entry.mappers:
            print(mapper.key, RegexpMapper(mapper, matches))


#re.sub(q[1], q[2].replace('$', '\\'), match) if match else None

"""
'regex' : r'(avast|avg)\/([\w\.]+)',                              # Avast/AVG Secure Browser
'props' : [['name', r'(.+)', '$1 Secure ' + 'Browser'], 'version'], 

'regex' : r'webkit.+?(mobile ?safari|safari)(\/[\w\.]+)', 
'props' : ['name', ['version', str_mapper, OLD_SAFARI_MAP]],        # Safari < 3.0 

'regex' : r'((?:avr32|ia64(?=;))|68k(?=\))|\barm(?=v(?:[1-7]|[5-7]1)l?|;|eabi)|(?=atmel )avr|(?:irix|mips|sparc)(?:64)?\b|pa-risc)',  
'props' : [['architecture', lowerize]]                              # IA64, 68K, ARM/64, AVR/32, IRIX/64, MIPS/64, SPARC/64, PA-RISC

'regex' : r'hbbtv\/\d+\.\d+\.\d+ +\([\w ]*; *(\w[^;]*);([^;]*)',                   # HbbTV devices
'props' : [['vendor', trim], ['model', trim], ['type', 'smarttv']], 

'regex' : r'(win(?=3|9|n)|win 9x )([nt\d\.]+)', 
'props' : [['name', 'Windows'], ['version', str_mapper, WINDOWS_VERSION_MAP]],
"""


REGEXES = {
    'browser': [
        {   
            'regex' : r'\b(?:crmo|crios)\/([\w\.]+)',                         # Chrome for Android/iOS
            'props' : ['version', ['name', 'Chrome']]
        },{ 
            'regex' : r'edg(?:e|ios|a)?\/([\w\.]+)',                          # Microsoft Edge
            'props' : ['version', ['name', 'Edge']]
        },{ 
            'regex' : r'(opera mini)\/([-\w\.]+)',                            # Opera Mini
            'props' : ['name', 'version']
        },{
            'regex' : r'(opera [mobiletab]{3,6})\b.+version\/([-\w\.]+)',     # Opera Mobi/Tablet
            'props' : ['name', 'version']
        },{
            'regex' : r'(opera)(?:.+version\/|[\/ ]+)([\w\.]+)',              # Opera
            'props' : ['name', 'version'] 
        },{ 
            'regex' : r'opios[\/ ]+([\w\.]+)',                              # Opera mini on iphone >= 8.0
            'props' : ['version', ['name', 'Opera' + ' Mini']], 
        },{ 
            'regex' : r'\bopr\/([\w\.]+)',                                  # Opera Webkit
            'props' : ['version', ['name', 'Opera']]
        },{ 
            'regex' : r'(kindle)\/([\w\.]+)',                                 # Kindle
            'props' : ['name', 'version']
        },{
            'regex' : r'(lunascape|maxthon|netfront|jasmine|blazer)[\/ ]?([\w\.]*)',  # Lunascape/Maxthon/Netfront/Jasmine/Blazer
            'props' : ['name', 'version']
        },{ 
            'regex' : r'(avant |iemobile|slim)(?:browser)?[\/ ]?([\w\.]*)',           # Avant/IEMobile/SlimBrowser
            'props' : ['name', 'version']
        },{
            'regex' : r'(ba?idubrowser)[\/ ]?([\w\.]+)',                              # Baidu Browser
            'props' : ['name', 'version']
        },{ 
            'regex' : r'(?:ms|\()(ie) ([\w\.]+)',                                     # Internet Explorer
            'props' : ['name', 'version']
        },{ 
            'regex' : r'(flock|rockmelt|midori|epiphany|silk|skyfire|ovibrowser|bolt|iron|vivaldi|iridium|phantomjs|bowser|quark|qupzilla|falkon|rekonq|puffin|brave|whale|qqbrowserlite|qq)\/([-\w\.]+)',  # Rekonq/Puffin/Brave/Whale/QQBrowserLite/QQ, aka ShouQ
            'props' : ['name', 'version']
        },{ 
            'regex' : r'(weibo)__([\d\.]+)',                                   # Weibo
            'props' : ['name', 'version']
        },{
            'regex' : r'(?:\buc? ?browser|(?:juc.+)ucweb)[\/ ]?([\w\.]+)',    # UCBrowser
            'props' : ['version', ['name', 'UC' + 'Browser']], 
        },{
            'regex' : r'\bqbcore\/([\w\.]+)',                                 # WeChat Desktop for Windows Built-in Browser
            'props' : ['version', ['name', 'WeChat(Win) Desktop']], 
        },{
            'regex' : r'micromessenger\/([\w\.]+)',                           # WeChat
            'props' : ['version', ['name', 'WeChat']], 
        },{
            'regex' : r'konqueror\/([\w\.]+)',                                # Konqueror
            'props' : ['version', ['name', 'Konqueror']], 
        },{
            'regex' : r'trident.+rv[: ]([\w\.]{1,9})\b.+like gecko',          # IE11
            'props' : ['version', ['name', 'IE']] 
        },{
            'regex' : r'yabrowser\/([\w\.]+)',                                # Yandex
            'props' : ['version', ['name', 'Yandex']], 
        },{
            'regex' : r'(avast|avg)\/([\w\.]+)',                              # Avast/AVG Secure Browser
            'props' : [['name', r'(.+)', '$1 Secure ' + 'Browser'], 'version'], 
        },{
            'regex' : r'\bfocus\/([\w\.]+)',                                  # Firefox Focus
            'props' : ['version', ['name', 'Firefox' + ' Focus']], 
        },{
            'regex' : r'\bopt\/([\w\.]+)',                                    # Opera Touch
            'props' : ['version', ['name', 'Opera' + ' Touch']], 
        },{
            'regex' :  r'coc_coc\w+\/([\w\.]+)',                              # Coc Coc Browser 
            'props' : ['version', ['name', 'Coc Coc']],
        },{
            'regex' : r'dolfin\/([\w\.]+)',                                   # Dolphin
            'props' : ['version', ['name', 'Dolphin']], 
        },{
            'regex' : r'coast\/([\w\.]+)',                                    # Opera Coast
            'props' : ['version', ['name', 'Opera' + ' Coast']], 
        },{
            'regex' : r'miuibrowser\/([\w\.]+)',                              # MIUI Browser
            'props' : ['version', ['name', 'MIUI ' + 'Browser']], 
        },{
            'regex' : r'fxios\/([-\w\.]+)',                                   # Firefox for iOS
            'props' : ['version', ['name', 'Firefox']], 
        },{
            'regex' : r'\bqihu|(qi?ho?o?|360)browser',                        # 360
            'props' : [['name', '360 ' + 'Browser']],  
        },{ 
            'regex' : r'(oculus|samsung|sailfish)browser\/([\w\.]+)',         # Oculus/Samsung/Sailfish Browser 
            'props' : [['name', r'(.+)', '$1 ' + 'Browser'], 'version'],
        },{
            'regex' : r'(comodo_dragon)\/([\w\.]+)',                          # Comodo Dragon
            'props' : [['name', r'_', ' '], 'version'], 
        },{
            'regex' : r'(electron)\/([\w\.]+) safari',                                # Electron-based App
            'props' : ['name', 'version']
        },{
            'regex' : r'(tesla)(?: qtcarbrowser|\/(20\d\d\.[-\w\.]+))',               # Tesla
            'props' : ['name', 'version']
        },{
            'regex' : r'm?(qqbrowser|baiduboxapp|2345Explorer)[\/ ]?([\w\.]+)',        # QQBrowser/Baidu App/2345 Browser
            'props' : ['name', 'version']
        },{
            'regex' : r'(metasr)[\/ ]?([\w\.]+)',                                     # SouGouBrowser
            'props' : ['name'], 
        },{
            'regex' : r'(lbbrowser)',                                                  # LieBao Browser
            'props' : ['name'], 
        },{
            'regex' : r'((?:fban\/fbios|fb_iab\/fb4a)(?!.+fbav)|;fbav\/([\w\.]+);)', 
            'props' : [['name', 'Facebook'], 'version'],                        # Facebook App for iOS & Android
        },{
            'regex' : r'safari (line)\/([\w\.]+)',                             # Line App for iOS
            'props' : ['name', 'version'], 
        },{
            'regex' : r'\b(line)\/([\w\.]+)\/iab',                                        # Line App for Android
            'props' : ['name', 'version'], 
        },{
            'regex' : r'(chromium|instagram)[\/ ]([-\w\.]+)',                              # Chromium/Instagram
            'props' : ['name', 'version'], 
        },{
            'regex' : r'\bgsa\/([\w\.]+) .*safari\/', 
            'props' : ['version', ['name', 'GSA']],                             # Google Search Appliance on iOS
        },{
            'regex' : r'headlesschrome(?:\/([\w\.]+)| )', 
            'props' : ['version', ['name', 'Chrome' + ' Headless']],            # Chrome Headless
        },{
            'regex' : r' wv\).+(chrome)\/([\w\.]+)', 
            'props' : [['name', 'Chrome' + ' WebView'], 'version'],             # Chrome WebView
        },{
            'regex' : r'droid.+ version\/([\w\.]+)\b.+(?:mobile safari|safari)', 
            'props' : ['version', ['name', 'Android ' + 'Browser']],            # Android Browser
        },{
            'regex' : r'(chrome|omniweb|arora|[tizenoka]{5} ?browser)\/v?([\w\.]+)', 
            'props' : ['name', 'version'],                                      # Chrome/OmniWeb/Arora/Tizen/Nokia
        },{
            'regex' : r'version\/([\w\.]+) .*mobile\/\w+ (safari)', 
            'props' : ['version', ['name', 'Mobile Safari']],                   # Mobile Safari
        },{
            'regex' : r'version\/([\w\.]+) .*(mobile ?safari|safari)', 
            'props' : ['version', 'name'],                                      # Safari & Safari Mobile
        },{
            'regex' : r'webkit.+?(mobile ?safari|safari)(\/[\w\.]+)', 
            'props' : ['name', ['version', str_mapper, OLD_SAFARI_MAP]],        # Safari < 3.0 
        },{
            'regex' : r'(webkit|khtml)\/([\w\.]+)', 
            'props' : ['name', 'version'], 
        },{
            'regex' : r'(navigator|netscape\d?)\/([-\w\.]+)', 
            'props' : [['name', 'Netscape'], 'version'],                        # Netscape 
        },{
            'regex' : r'mobile vr; rv:([\w\.]+)\).+firefox', 
            'props' : ['version', ['name', 'Firefox' + ' Reality']],            # Firefox Reality
        },{
            'regex' : r'ekiohf.+(flow)\/([\w\.]+)',                                   # Flow
            'props' : ['name', 'version']
        },{
            'regex' : r'(swiftfox)',                                                  # Swiftfox
            'props' : ['name', 'version']
        },{
            'regex' : r'(icedragon|iceweasel|camino|chimera|fennec|maemo browser|minimo|conkeror|klar)[\/ ]?([\w\.\+]+)',                         # IceDragon/Iceweasel/Camino/Chimera/Fennec/Maemo/Minimo/Conkeror/Klar
            'props' : ['name', 'version']
        },{
            'regex' : r'(seamonkey|k-meleon|icecat|iceape|firebird|phoenix|palemoon|basilisk|waterfox)\/([-\w\.]+)$',                             # Firefox/SeaMonkey/K-Meleon/IceCat/IceApe/Firebird/Phoenix
            'props' : ['name', 'version']
        },{
            'regex' : r'(firefox)\/([\w\.]+)',                                        # Other Firefox-based
            'props' : ['name', 'version']
        },{
            'regex' : r'(mozilla)\/([\w\.]+) .+rv\:.+gecko\/\d+',                     # Mozilla
            'props' : ['name', 'version']
        },{
            'regex' : r'(polaris|lynx|dillo|icab|doris|amaya|w3m|netsurf|sleipnir|obigo|mosaic|(?:go|ice|up)[\. ]?browser)[-\/ ]?v?([\w\.]+)',    # Polaris/Lynx/Dillo/iCab/Doris/Amaya/w3m/NetSurf/Sleipnir/Obigo/Mosaic/Go/ICE/UP.Browser
            'props' : ['name', 'version']
        },{
            'regex' : r'(links) \(([\w\.]+)',                                          # Links
            'props' : ['name', 'version']
        }
    ],

    'cpu': [
        {
            'regex' : r'(?:(amd|x(?:(?:86|64)[-_])?|wow|win)64)[;\)]',        # AMD64 (x64)
            'props' : [['architecture', 'amd64']],                              
        },{
            'regex' : r'(ia32(?=;))',                                         # IA32 (quicktime)
            'props' : [['architecture', lowerize]],                             
        },{
            'regex' : r'((?:i[346]|x)86)[;\)]',                               # IA32 (x86)
            'props' : [['architecture', 'ia32']], 
        },{
            'regex' : r'\b(aarch64|arm(v?8e?l?|_?64))\b',                     # ARM64
            'props' : [['architecture', 'arm64']], 
        },{
            'regex' : r'\b(arm(?:v[67])?ht?n?[fl]p?)\b',                      # ARMHF
            'props' : [['architecture', 'armhf']], 
        },{
            'regex' : r'windows (ce|mobile); ppc;',                           # PocketPC mistakenly identified as PowerPC
            'props' : [['architecture', 'arm']],  
        },{
            'regex' : r'((?:ppc|powerpc)(?:64)?)(?: mac|;|\))',               # PowerPC
            'props' : [['architecture', r'ower', EMPTY, lowerize]], 
        },{
            'regex' : r'(sun4\w)[;\)]',                                       # SPARC
            'props' : [['architecture', 'sparc']], 
        },{
            'regex' : r'((?:avr32|ia64(?=;))|68k(?=\))|\barm(?=v(?:[1-7]|[5-7]1)l?|;|eabi)|(?=atmel )avr|(?:irix|mips|sparc)(?:64)?\b|pa-risc)',  
            'props' : [['architecture', lowerize]]                              # IA64, 68K, ARM/64, AVR/32, IRIX/64, MIPS/64, SPARC/64, PA-RISC
        }
    ], 

    'device': [
        {
            'regex' : r'\b(sch-i[89]0\d|shw-m380s|sm-[pt]\w{2,4}|gt-[pn]\d{2,4}|sgh-t8[56]9|nexus 10)',   # Samsung devices 
            'props' : ['model', ['vendor', 'Samsung'], ['type', 'tablet']], 
        },{
            'regex' : r'\b((?:s[cgp]h|gt|sm)-\w+|galaxy nexus)', 
            'props' : ['model', ['vendor', 'Samsung'], ['type', 'mobile']], 
            },{
            'regex' : r'samsung[- ]([-\w]+)', 
            'props' : ['model', ['vendor', 'Samsung'], ['type', 'mobile']], 
            },{
            'regex' : r'sec-(sgh\w+)', 
            'props' : ['model', ['vendor', 'Samsung'], ['type', 'mobile']], 
        },{
            'regex' : r'\((ip(?:hone|od)[\w ]*);',                                    # iPod/iPhone
            'props' : ['model', ['vendor', 'Apple'], ['type', 'mobile']],
        },{
            'regex' : r'\((ipad);[-\w\),; ]+apple',                                           # iPad
            'props' : ['model', ['vendor', 'Apple'], ['type', 'tablet']], 
        },{
            'regex' : r'applecoremedia\/[\w\.]+ \((ipad)', 
            'props' : ['model', ['vendor', 'Apple'], ['type', 'tablet']], 
        },{
            'regex' : r'\b(ipad)\d\d?,\d\d?[;\]].+ios', 
            'props' : ['model', ['vendor', 'Apple'], ['type', 'tablet']], 
        },{
            'regex' : r'\b((?:ag[rs][23]?|bah2?|sht?|btv)-a?[lw]\d{2})\b(?!.+d\/s)',  # Huawei
            'props' : ['model', ['vendor', 'Huawei'], ['type', 'tablet']], 
        },{
            'regex' : r'(?:huawei|honor)([-\w ]+)[;\)]', 
            'props' : ['model', ['vendor', 'Huawei'], ['type', 'mobile']], 
        },{
            'regex' : r'\b(nexus 6p|\w{2,4}-[atu]?[ln][01259x][012359][an]?)\b(?!.+d\/s)', 
            'props' : ['model', ['vendor', 'Huawei'], ['type', 'mobile']],
        },{
            'regex' : r'\b(poco[\w ]+)(?: bui|\))',                                           # Xiaomi POCO
            'props' : [['model', '_', ' '], ['vendor', 'Xiaomi'], ['type', 'mobile']], 
        },{
            'regex' : r'\b; (\w+) build\/hm\1',                                               # Xiaomi Hongmi 'numeric' models
            'props' : [['model', '_', ' '], ['vendor', 'Xiaomi'], ['type', 'mobile']], 
        },{
            'regex' : r'\b(hm[-_ ]?note?[_ ]?(?:\d\w)?) bui',                                 # Xiaomi Hongmi
            'props' : [['model', '_', ' '], ['vendor', 'Xiaomi'], ['type', 'mobile']], 
        },{
            'regex' : r'\b(redmi[\-_ ]?(?:note|k)?[\w_ ]+)(?: bui|\))',                       # Xiaomi Redmi
            'props' : [['model', '_', ' '], ['vendor', 'Xiaomi'], ['type', 'mobile']], 
        },{
            'regex' : r'\b(mi[-_ ]?(?:a\d|one|one[_ ]plus|note lte|max)?[_ ]?(?:\d?\w?)[_ ]?(?:plus|se|lite)?)(?: bui|\))',  # Xiaomi Mi
            'props' : [['model', '_', ' '], ['vendor', 'Xiaomi'], ['type', 'mobile']], 
        },{
            'regex' : r'\b(mi[-_ ]?(?:pad)(?:[\w_ ]+))(?: bui|\))',                   # Mi Pad tablets
            'props' : [['model', '_', ' '], ['vendor', 'Xiaomi'], ['type', 'tablet']], 
        },{
            'regex' : r'; (\w+) bui.+ oppo',                                                  # OPPO
            'props' : ['model', ['vendor', 'OPPO'], ['type', 'mobile']]
        },{
            'regex' : r'\b(cph[12]\d{3}|p(?:af|c[al]|d\w|e[ar])[mt]\d0|x9007|a101op)\b', 
            'props' : ['model', ['vendor', 'OPPO'], ['type', 'mobile']], 
        },{
            'regex' : r'vivo (\w+)(?: bui|\))',                                               # Vivo
            'props' : ['model', ['vendor', 'Vivo'], ['type', 'mobile']], 
        },{ 
            'regex' : r'\b(v[12]\d{3}\w?[at])(?: bui|;)',
            'props' : ['model', ['vendor', 'Vivo'], ['type', 'mobile']], 
        },{
            'regex' : r'\b(rmx[12]\d{3})(?: bui|;|\))',                               # Realme
            'props' : ['model', ['vendor', 'Realme'], ['type', 'mobile']], 
        },{
            'regex' : r'\b(milestone|droid(?:[2-4x]| (?:bionic|x2|pro|razr))?:?( 4g)?)\b[\w ]+build\/', # Motorola
            'props' : ['model', ['vendor', 'Motorola'], ['type', 'mobile']], 
        },{ 
            'regex' : r'\bmot(?:orola)?[- ](\w*)',
            'props' : ['model', ['vendor', 'Motorola'], ['type', 'mobile']], 
        },{ 
            'regex' : r'((?:moto[\w\(\) ]+|xt\d{3,4}|nexus 6)(?= bui|\)))',
            'props' : ['model', ['vendor', 'Motorola'], ['type', 'mobile']] 
        },{
            'regex' : r'\b(mz60\d|xoom[2 ]{0,2}) build\/', 
            'props' : ['model', ['vendor', 'Motorola'], ['type', 'tablet']], 
        },{
            'regex' : r'((?=lg)?[vl]k\-?\d{3}) bui| 3\.[-\w; ]{10}lg?-([06cv9]{3,4})', # 'LG'
            'props' : ['model', ['vendor', 'LG'], ['type', 'tablet']], 
        },{
            'regex' : r'(lm(?:-?f100[nv]?|-[\w\.]+)(?= bui|\))|nexus [45])',
            'props' : ['model', ['vendor', 'LG'], ['type', 'mobile']], 
        },{
            'regex' : r'\blg[-e;\/ ]+((?!browser|netcast|android tv)\w+)',
            'props' : ['model', ['vendor', 'LG'], ['type', 'mobile']], 
        },{
            'regex' : r'\blg-?([\d\w]+) bui', 
            'props' : ['model', ['vendor', 'LG'], ['type', 'mobile']], 
        },{
            'regex' : r'(ideatab[-\w ]+)',                                                    # Lenovo 
            'props' : ['model', ['vendor', 'Lenovo'], ['type', 'tablet']], 
        },{
            'regex' : r'lenovo ?(s[56]000[-\w]+|tab(?:[\w ]+)|yt[-\d\w]{6}|tb[-\d\w]{6})', 
            'props' : ['model', ['vendor', 'Lenovo'], ['type', 'tablet']], 
        },{
            'regex' : r'(?:maemo|nokia).*(n900|lumia \d+)',                                   # Nokia
            'props' : [['model', '_', ' '], ['vendor', 'Nokia'], ['type', 'mobile']], 
        },{
            'regex' : r'nokia[-_ ]?([-\w\.]*)', 
            'props' : [['model', '_', ' '], ['vendor', 'Nokia'], ['type', 'mobile']], 
        },{
            'regex' : r'(pixel c)\b',                                                 # Google Pixel C
            'props' : ['model', ['vendor', 'Google'], ['type', 'tablet']], 
        },{
            'regex' : r'droid.+; (pixel[\daxl ]{0,6})(?: bui|\))',                    # Google Pixel
            'props' : ['model', ['vendor', 'Google'], ['type', 'mobile']], 
        },{
            'regex' : r'droid.+ ([c-g]\d{4}|so[-gl]\w+|xq-a\w[4-7][12])(?= bui|\).+chrome\/(?![1-6]{0,1}\d\.))', # Sony
            'props' : ['model', ['vendor', 'Sony'], ['type', 'mobile']], 
        },{
            'regex' : r'sony tablet [ps]', 
            'props' : [['model', 'Xperia Tablet'], ['vendor', 'Sony'], ['type', 'tablet']], 
        },{
            'regex' : r'\b(?:sony)?sgp\w+(?: bui|\))', 
            'props' : [['model', 'Xperia Tablet'], ['vendor', 'Sony'], ['type', 'tablet']], 
        },{
            'regex' : r' (kb2005|in20[12]5|be20[12][59])\b',                                  # OnePlus
            'props' : ['model', ['vendor', 'OnePlus'], ['type', 'mobile']], 
        },{
            'regex' : r'(?:one)?(?:plus)? (a\d0\d\d)(?: b|\))', 
            'props' : ['model', ['vendor', 'OnePlus'], ['type', 'mobile']], 
        },{
            'regex' : r'(alexa)webm',                                                         # Amazon
            'props' : ['model', ['vendor', 'Amazon'], ['type', 'tablet']], 
        },{
            'regex' : r'(kf[a-z]{2}wi)( bui|\))',                                             # Kindle Fire without Silk
            'props' : ['model', ['vendor', 'Amazon'], ['type', 'tablet']], 
        },{
            'regex' : r'(kf[a-z]+)( bui|\)).+silk\/',                                          # Kindle Fire HD
            'props' : ['model', ['vendor', 'Amazon'], ['type', 'tablet']], 
        },{
            'regex' : r'((?:sd|kf)[0349hijorstuw]+)( bui|\)).+silk\/',                # Fire Phone
            'props' : [['model', r'(.+)', 'Fire Phone $1'], ['vendor', 'Amazon'], ['type', 'mobile']], 
        },{
            'regex' : r'(playbook);[-\w\),; ]+(rim)',                                 # BlackBerry PlayBook
            'props' : ['model', 'vendor', ['type', 'tablet']],
        },{
            'regex' : r'\b((?:bb[a-f]|st[hv])100-\d)',                                    # BlackBerry 10
            'props' : ['model', ['vendor', 'BlackBerry'], ['type', 'mobile']], 
        },{
            'regex' : r'\(bb10; (\w+)',                                                        # BlackBerry 10
            'props' : ['model', ['vendor', 'BlackBerry'], ['type', 'mobile']], 
        },{
            'regex' : r'(?:\b|asus_)(transfo[prime ]{4,10} \w+|eeepc|slider \w+|nexus 7|padfone|p00[cj])', # Asus
            'props' : ['model', ['vendor', 'ASUS'], ['type', 'tablet']], 
        },{
            'regex' : r' (z[bes]6[027][012][km][ls]|zenfone \d\w?)\b', 
            'props' : ['model', ['vendor', 'ASUS'], ['type', 'mobile']], 
        },{
            'regex' : r'(nexus 9)',                                                   # HTC Nexus 9
            'props' : ['model', ['vendor', 'HTC'], ['type', 'tablet']], 
        },{
            'regex' : r'(htc)[-;_ ]{1,2}([\w ]+(?=\)| bui)|\w+)',                             # HTC
            'props' : ['vendor', ['model', '_', ' '], ['type', 'mobile']], 
        },{
            'regex' : r'(zte)[- ]([\w ]+?)(?: bui|\/|\))',                                    # ZTE
            'props' : ['vendor', ['model', '_', ' '], ['type', 'mobile']], 
        },{
            'regex' : r'(alcatel|geeksphone|nexian|panasonic|sony)[-_ ]?([-\w]*)',             # Alcatel/GeeksPhone/Nexian/Panasonic/Sony
            'props' : ['vendor', ['model', '_', ' '], ['type', 'mobile']], 
        },{
            'regex' : r'droid.+; ([ab][1-7]-?[0178a]\d\d?)',                          # Acer
            'props' : ['model', ['vendor', 'Acer'], ['type', 'tablet']], 
        },{
            'regex' : r'\bmz-([-\w]{2,})',                                          # Meizu
            'props' : ['model', ['vendor', 'Meizu'], ['type', 'mobile']], 
        },{
            'regex' : r'droid.+; (m[1-5] note) bui',                                # Meizu
            'props' : ['model', ['vendor', 'Meizu'], ['type', 'mobile']], 
        },{
            'regex' : r'\b(sh-?[altvz]?\d\d[a-ekm]?)',                                # Sharp
            'props' : ['model', ['vendor', 'Sharp'], ['type', 'mobile']], 
        },{
            'regex' : r'(blackberry|benq|palm(?=\-)|sonyericsson|acer|asus|dell|meizu|motorola|polytron)[-_ ]?([-\w]*)',  # BlackBerry/BenQ/Palm/Sony-Ericsson/Acer/Asus/Dell/Meizu/Motorola/Polytron
            'props' : ['vendor', 'model', ['type', 'mobile']], 
        },{
            'regex' : r'(hp) ([\w ]+\w)',                                                     # HP iPAQ
            'props' : ['vendor', 'model', ['type', 'mobile']], 
        },{ 
            'regex' : r'(asus)-?(\w+)',                                                       # Asus
            'props' : ['vendor', 'model', ['type', 'mobile']], 
        },{
            'regex' : r'(microsoft); (lumia[\w ]+)',                                          # Microsoft Lumia
            'props' : ['vendor', 'model', ['type', 'mobile']], 
        },{
            'regex' : r'(lenovo)[-_ ]?([-\w]+)',                                              # Lenovo
            'props' : ['vendor', 'model', ['type', 'mobile']], 
        },{
            'regex' : r'(jolla)',                                                             # Jolla
            'props' : ['vendor', 'model', ['type', 'mobile']], 
        },{
            'regex' : r'(oppo) ?([\w ]+) bui',                                                 # OPPO
            'props' : ['vendor', 'model', ['type', 'mobile']], 
        },{
            'regex' : r'(archos) (gamepad2?)',                                                # Archos
            'props' : ['vendor', 'model', ['type', 'tablet']], 
        },{
            'regex' : r'(hp).+(touchpad(?!.+tablet)|tablet)',                                 # HP TouchPad
            'props' : ['vendor', 'model', ['type', 'tablet']], 
        },{
            'regex' : r'(kindle)\/([\w\.]+)',                                                 # Kindle
            'props' : ['vendor', 'model', ['type', 'tablet']], 
        },{ 
            'regex' : r'(nook)[\w ]+build\/(\w+)',                                            # Nook
            'props' : ['vendor', 'model', ['type', 'tablet']], 
        },{
            'regex' : r'(dell) (strea[kpr\d ]*[\dko])',                                       # Dell Streak
            'props' : ['vendor', 'model', ['type', 'tablet']], 
        },{
            'regex' : r'(le[- ]+pan)[- ]+(\w{1,9}) bui',                                      # Le Pan Tablets
            'props' : ['vendor', 'model', ['type', 'tablet']], 
        },{ 
            'regex' : r'(trinity)[- ]*(t\d{3}) bui',                                          # Trinity Tablets
            'props' : ['vendor', 'model', ['type', 'tablet']], 
        },{
            'regex' : r'(gigaset)[- ]+(q\w{1,9}) bui',                                        # Gigaset Tablets
            'props' : ['vendor', 'model', ['type', 'tablet']], 
        },{ 
            'regex' : r'(vodafone) ([\w ]+)(?:\)| bui)',                                       # Vodafone
            'props' : ['vendor', 'model', ['type', 'tablet']], 
        },{
            'regex' : r'(surface duo)',                                               # Surface Duo
            'props' : ['model', ['vendor', 'Microsoft'], ['type', 'tablet']], 
        },{
            'regex' : r'droid [\d\.]+; (fp\du?)(?: b|\))',                            # Fairphone
            'props' : ['model', ['vendor', 'Fairphone'], ['type', 'mobile']], 
        },{
            'regex' : r'(u304aa)',                                                    # AT&T
            'props' : ['model', ['vendor', 'AT&T'], ['type', 'mobile']],  
        },{
            'regex' : r'\bsie-(\w*)',                                                 # Siemens
            'props' : ['model', ['vendor', 'Siemens'], ['type', 'mobile']], 
        },{
            'regex' : r'\b(rct\w+) b',                                                # RCA Tablets
            'props' : ['model', ['vendor', 'RCA'], ['type', 'tablet']], 
        },{
            'regex' : r'\b(venue[\d ]{2,7}) b',                                       # Dell Venue Tablets
            'props' : ['model', ['vendor', 'Dell'], ['type', 'tablet']], 
        },{
            'regex' : r'\b(q(?:mv|ta)\w+) b',                                         # Verizon Tablet
            'props' : ['model', ['vendor', 'Verizon'], ['type', 'tablet']], 
        },{
            'regex' : r'\b(?:barnes[& ]+noble |bn[rt])([\w\+ ]*) b',                  # Barnes & Noble Tablet
            'props' : ['model', ['vendor', 'Barnes & Noble'], ['type', 'tablet']], 
        },{
            'regex' : r'\b(tm\d{3}\w+) b',
            'props' : ['model', ['vendor', 'NuVision'], ['type', 'tablet']], 
        },{
            'regex' : r'\b(k88) b',                                                   # ZTE K Series Tablet
            'props' : ['model', ['vendor', 'ZTE'], ['type', 'tablet']], 
        },{
            'regex' : r'\b(nx\d{3}j) b',                                              # ZTE Nubia
            'props' : ['model', ['vendor', 'ZTE'], ['type', 'mobile']], 
        },{
            'regex' : r'\b(gen\d{3}) b.+49h',                                         # Swiss GEN Mobile
            'props' : ['model', ['vendor', 'Swiss'], ['type', 'mobile']], 
        },{
            'regex' : r'\b(zur\d{3}) b',                                              # Swiss ZUR Tablet
            'props' : ['model', ['vendor', 'Swiss'], ['type', 'tablet']], 
        },{
            'regex' : r'\b((zeki)?tb.*\b) b',                                         # Zeki Tablets
            'props' : ['model', ['vendor', 'Zeki'], ['type', 'tablet']], 
        },{
            'regex' : r'\b([yr]\d{2}) b',                                             # Dragon Touch Tablet
            'props' : [['vendor', 'Dragon Touch'], 'model', ['type', 'tablet']], 
        },{
            'regex' : r'\b(dragon[- ]+touch |dt)(\w{5}) b',                           # Dragon Touch Tablet
            'props' : [['vendor', 'Dragon Touch'], 'model', ['type', 'tablet']], 
        },{
            'regex' : r'\b(ns-?\w{0,9}) b',                                           # Insignia Tablets
            'props' : ['model', ['vendor', 'Insignia'], ['type', 'tablet']], 
        },{
            'regex' : r'\b((nxa|next)-?\w{0,9}) b',                                   # NextBook Tablets
            'props' : ['model', ['vendor', 'NextBook'], ['type', 'tablet']], 
        },{
            'regex' : r'\b(xtreme\_)?(v(1[045]|2[015]|[3469]0|7[05])) b',             # Voice Xtreme Phones
            'props' : [['vendor', 'Voice'], 'model', ['type', 'mobile']], 
        },{
            'regex' : r'\b(lvtel\-)?(v1[12]) b',                                      # LvTel Phones
            'props' : [['vendor', 'LvTel'], 'model', ['type', 'mobile']], 
        },{
            'regex' : r'\b(ph-1) ',                                                   # Essential PH-1
            'props' : ['model', ['vendor', 'Essential'], ['type', 'mobile']], 
        },{
            'regex' : r'\b(v(100md|700na|7011|917g).*\b) b',                          # Envizen Tablets
            'props' : ['model', ['vendor', 'Envizen'], ['type', 'tablet']], 
        },{
            'regex' : r'\b(trio[-\w\. ]+) b',                                         # MachSpeed Tablets
            'props' : ['model', ['vendor', 'MachSpeed'], ['type', 'tablet']], 
        },{
            'regex' : r'\btu_(1491) b',                                               # Rotor Tablets
            'props' : ['model', ['vendor', 'Rotor'], ['type', 'tablet']], 
        },{
            'regex' : r'(shield[\w ]+) b',                                            # Nvidia Shield Tablets
            'props' : ['model', ['vendor', 'Nvidia'], ['type', 'tablet']], 
        },{
            'regex' : r'(sprint) (\w+)',                                              # Sprint Phones
            'props' : ['vendor', 'model', ['type', 'mobile']], 
        },{
            'regex' : r'(kin\.[onetw]{3})',                                           # Microsoft Kin
            'props' : [['model', r'\.', ' '], ['vendor', 'Microsoft'], ['type', 'mobile']], 
        },{
            'regex' : r'droid.+; (cc6666?|et5[16]|mc[239][23]x?|vc8[03]x?)\)',        # Zebra
            'props' : ['model', ['vendor', 'Zebra'], ['type', 'tablet']], 
        },{
            'regex' : r'droid.+; (ec30|ps20|tc[2-8]\d[kx])\)', 
            'props' : ['model', ['vendor', 'Zebra'], ['type', 'mobile']], 
        },{
            'regex' : r'(ouya)',                                                              # Ouya
            'props' : ['vendor', 'model', ['type', 'console']],  
        },{
            'regex' : r'(nintendo) ([wids3utch]+)',                                          # Nintendo
            'props' : ['vendor', 'model', ['type', 'console']],  
        },{
            'regex' : r'droid.+; (shield) bui',                                       # Nvidia
            'props' : ['model', ['vendor', 'Nvidia'], ['type', 'console']], 
        },{
            'regex' : r'(playstation [345portablevi]+)',                              # Playstation
            'props' : ['model', ['vendor', 'Sony'], ['type', 'console']],  
        },{
            'regex' : r'\b(xbox(?: one)?(?!; xbox))[\); ]',                           # Microsoft Xbox
            'props' : ['model', ['vendor', 'Microsoft'], ['type', 'console']],  
        },{
            'regex' : r'smart-tv.+(samsung)',                                         # Samsung SmartTV
            'props' : ['vendor', ['type', 'smarttv']], 
        },{
            'regex' : r'hbbtv.+maple;(\d+)',
            'props' : [['model', '^', 'SmartTV'], ['vendor', 'Samsung'], ['type', 'smarttv']],  
        },{
            'regex' : r'(nux; netcast.+smarttv|lg (netcast\.tv-201\d|android tv))',   # 'LG' SmartTV
            'props' : [['vendor', 'LG'], ['type', 'smarttv']],  
        },{
            'regex' : r'(apple) ?tv',                                                 # Apple TV
            'props' : ['vendor', ['model', 'Apple' + ' TV'], ['type', 'smarttv']],  
        },{
            'regex' : r'crkey',                                                       # Google Chromecast
            'props' : [['model', 'Chrome' + 'cast'], ['vendor', 'Google'], ['type', 'smarttv']],  
        },{
            'regex' : r'droid.+aft(\w)( bui|\))',                                     # Fire TV
            'props' : ['model', ['vendor', 'Amazon'], ['type', 'smarttv']],  
        },{
            'regex' : r'\(dtv[\);].+(aquos)',                                         # Sharp
            'props' : ['model', ['vendor', 'Sharp'], ['type', 'smarttv']],  
        },{
            'regex' : r'\b(roku)[\dx]*[\)\/]((?:dvp-)?[\d\.]*)',                              # Roku
            'props' : [['vendor', trim], ['model', trim], ['type', 'smarttv']],  
        },{
            'regex' : r'hbbtv\/\d+\.\d+\.\d+ +\([\w ]*; *(\w[^;]*);([^;]*)',                   # HbbTV devices
            'props' : [['vendor', trim], ['model', trim], ['type', 'smarttv']],  
        },{
            'regex' : r'\b(android tv|smart[- ]?tv|opera tv|tv; rv:)\b',              # SmartTV from Unidentified Vendors
            'props' : [['type', 'smarttv']],  
        },{
            'regex' : r'((pebble))app',                                               # Pebble
            'props' : ['vendor', 'model', ['type', 'wearable']], 
        },{
            'regex' : r'droid.+; (glass) \d',                                         # Google Glass
            'props' : ['model', ['vendor', 'Google'], ['type', 'wearable']],  
        },{
            'regex' : r'droid.+; (wt63?0{2,3})\)',
            'props' : ['model', ['vendor', 'Zebra'], ['type', 'wearable']],  
        },{
            'regex' : r'(quest( 2)?)',                                                # Oculus Quest
            'props' : ['model', ['vendor', 'Facebook'], ['type', 'wearable']],  
        },{
            'regex' : r'(tesla)(?: qtcarbrowser|\/[-\w\.]+)',                         # Tesla
            'props' : ['vendor', ['type', 'embedded']],  
        },{
            'regex' : r'droid .+?; ([^;]+?)(?: bui|\) applew).+? mobile safari',      # Android Phones from Unidentified Vendors
            'props' : ['model', ['type', 'mobile']],  
        },{
            'regex' : r'droid .+?; ([^;]+?)(?: bui|\) applew).+?(?! mobile) safari',  # Android Tablets from Unidentified Vendors
            'props' : ['model', ['type', 'tablet']],  
        },{
            'regex' : r'\b((tablet|tab)[;\/]|focus\/\d(?!.+mobile))',                 # Unidentifiable Tablet
            'props' : [['type', 'tablet']],  
        },{
            'regex' : r'(phone|mobile(?:[;\/]| safari)|pda(?=.+windows ce))',         # Unidentifiable Mobile
            'props' : [['type', 'mobile']],  
        },{
            'regex' : r'(android[-\w\. ]{0,9});.+buil',                                # Generic Android Device
            'props' : ['model', ['vendor', 'Generic']]
        }
    ],

    'engine': [
        {
            'regex' : r'windows.+ edge\/([\w\.]+)',                           # EdgeHTML
            'props' : ['version', ['name', 'Edge' + 'HTML']], 
        },{
            'regex' : r'webkit\/537\.36.+chrome\/(?!27)([\w\.]+)',            # Blink
            'props' : ['version', ['name', 'Blink']], 
        },{
            'regex' : r'(presto)\/([\w\.]+)',                                         # Presto
            'props' : ['name', 'version'], 
        },{
            'regex' : r'(webkit|trident|netfront|netsurf|amaya|lynx|w3m|goanna)\/([\w\.]+)',  # WebKit/Trident/NetFront/NetSurf/Amaya/Lynx/w3m/Goanna
            'props' : ['name', 'version'], 
        },{
            'regex' : r'ekioh(flow)\/([\w\.]+)',                                      # Flow
            'props' : ['name', 'version'], 
        },{
            'regex' : r'(khtml|tasman|links)[\/ ]\(?([\w\.]+)',                       # KHTML/Tasman/Links
            'props' : ['name', 'version'], 
        },{
            'regex' : r'(icab)[\/ ]([23]\.[\d\.]+)',                                   # iCab 
            'props' : ['name', 'version'], 
        },{
            'regex' : r'rv\:([\w\.]{1,9})\b.+(gecko)',                        # Gecko
            'props' : ['version', 'name']
        }
    ],

    'os': [
        {
            'regex' : r'microsoft (windows) (vista|xp)',                            # Windows (iTunes)
            'props' : ['name', 'version'],
        },{
            'regex' : r'(windows) nt 6\.2; (arm)',                                    # Windows RT
            'props' : ['name', ['version', str_mapper, WINDOWS_VERSION_MAP]], 
        },{
            'regex' : r'(windows (?:phone(?: os)?|mobile))[\/ ]?([\d\.\w ]*)',        # Windows Phone
            'props' : ['name', ['version', str_mapper, WINDOWS_VERSION_MAP]], 
        },{
            'regex' : r'(windows)[\/ ]?([ntce\d\. ]+\w)(?!.+xbox)',
            'props' : ['name', ['version', str_mapper, WINDOWS_VERSION_MAP]], 
        },{
            'regex' : r'(win(?=3|9|n)|win 9x )([nt\d\.]+)', 
            'props' : [['name', 'Windows'], ['version', str_mapper, WINDOWS_VERSION_MAP]],
        },{
            'regex' : r'ip[honead]{2,4}\b(?:.*os ([\w]+) like mac|; opera)',          # iOS
            'props' : [['version', '_', '.'], ['name', 'iOS']], 
        },{
            'regex' : r'cfnetwork\/.+darwin',
            'props' : [['version', '_', '.'], ['name', 'iOS']], 
        },{
            'regex' : r'(mac os x) ?([\w\. ]*)',                                    # Mac OS
            'props' : [['name', 'Mac OS'], ['version', '_', '.']],
        },{ 
            'regex' : r'(macintosh|mac_powerpc\b)(?!.+haiku)',                      # Mac OS
            'props' : [['name', 'Mac OS'], ['version', '_', '.']],
        },{ 
            'regex' : r'droid ([\w\.]+)\b.+(android[- ]x86)',                 # Android-x86
            'props' : ['version', 'name'], 
        },{
            'regex' : r'(android|webos|qnx|bada|rim tablet os|maemo|meego|sailfish)[-\/ ]?([\w\.]*)',  # Android/WebOS/QNX/Bada/RIM/Maemo/MeeGo/Sailfish OS
            'props' : ['name', 'version'], 
        },{
            'regex' : r'(blackberry)\w*\/([\w\.]*)',                                  # Blackberry
            'props' : ['name', 'version'], 
        },{
            'regex' : r'(tizen|kaios)[\/ ]([\w\.]+)',                                 # Tizen/KaiOS
            'props' : ['name', 'version'], 
        },{
            'regex' : r'\((series40);',                                                # Series 40
            'props' : ['name', 'version'], 
        },{
            'regex' : r'\(bb(10);',                                           # BlackBerry 10
            'props' : ['version', ['name', 'BlackBerry']], 
        },{
            'regex' : r'(?:symbian ?os|symbos|s60(?=;)|series60)[-\/ ]?([\w\.]*)',  # Symbian
            'props' : ['version', ['name', 'Symbian']], 
        },{
            'regex' : r'mozilla\/[\d\.]+ \((?:mobile|tablet|tv|mobile; [\w ]+); rv:.+ gecko\/([\w\.]+)',  # Firefox OS
            'props' : ['version', ['name', 'Firefox' + ' OS']], 
        },{
            'regex' : r'web0s;.+rt(tv)',                                            # WebOS
            'props' : ['version', ['name', 'webOS']], 
        },{
            'regex' : r'\b(?:hp)?wos(?:browser)?\/([\w\.]+)',                          # WebOS
            'props' : ['version', ['name', 'webOS']], 
        },{
            'regex' : r'crkey\/([\d\.]+)',                                    # Google Chromecast
            'props' : ['version', ['name', 'Chrome' + 'cast']], 
        },{
            'regex' : r'(cros) [\w]+ ([\w\.]+\w)',                            # Chromium OS
            'props' : [['name', 'Chromium OS'], 'version'], 
        },{
            'regex' : r'(nintendo|playstation) ([wids345portablevuch]+)',             # Nintendo/Playstation
            'props' : ['name', 'version'], 
        },{ 
            'regex' : r'(xbox); +xbox ([^\);]+)',                                     # Microsoft Xbox (360, One, X, S, Series X, Series S)
            'props' : ['name', 'version'], 
        },{ 
            'regex' : '\b(joli|palm)\b ?(?:os)?\/?([\w\.]*)',                        # Joli/Palm
            'props' : ['name', 'version'], 
        },{ 
            'regex' : r'(mint)[\/\(\) ]?(\w*)',                                       # Mint
            'props' : ['name', 'version'], 
        },{ 
            'regex' : r'(mageia|vectorlinux)[; ]',                                    # Mageia/VectorLinux
            'props' : ['name', 'version'], 
        },{ 
            'regex' : r'([kxln]?ubuntu|debian|suse|opensuse|gentoo|arch(?= linux)|slackware|fedora|mandriva|centos|pclinuxos|red ?hat|zenwalk|linpus|raspbian|plan 9|minix|risc os|contiki|deepin|manjaro|elementary os|sabayon|linspire)(?: gnu\/linux)?(?: enterprise)?(?:[- ]linux)?(?:-gnu)?[-\/ ]?(?!chrom|package)([-\w\.]*)',  # Ubuntu/Debian/SUSE/Gentoo/Arch/Slackware/Fedora/Mandriva/CentOS/PCLinuxOS/RedHat/Zenwalk/Linpus/Raspbian/Plan9/Minix/RISCOS/Contiki/Deepin/Manjaro/elementary/Sabayon/Linspire
            'props' : ['name', 'version'], 
        },{
            'regex' : r'(hurd|linux) ?([\w\.]*)',                                     # Hurd/Linux
            'props' : ['name', 'version'], 
        },{ 
            'regex' : r'(gnu) ?([\w\.]*)',                                            # GNU
            'props' : ['name', 'version'], 
        },{ 
            'regex' : r'\b([-frentopcghs]{0,5}bsd|dragonfly)[\/ ]?(?!amd|[ix346]{1,2}86)([\w\.]*)',  # FreeBSD/NetBSD/OpenBSD/PC-BSD/GhostBSD/DragonFly
            'props' : ['name', 'version'], 
        },{
            'regex' : r'(haiku) (\w+)',                                                # Haiku
            'props' : ['name', 'version'], 
        },{
            'regex' : r'(sunos) ?([\w\.\d]*)',                                # Solaris
            'props' : [['name', 'Solaris'], 'version'], 
        },{
            'regex' : r'((?:open)?solaris)[-\/ ]?([\w\.]*)',                          # Solaris
            'props' : ['name', 'version']
        },{
            'regex' : r'(aix) ((\d)(?=\.|\)| )[\w\.])*',                              # AIX
            'props' : ['name', 'version']
        },{
            'regex' : r'\b(beos|os\/2|amigaos|morphos|openvms|fuchsia|hp-ux)',        # BeOS/OS2/AmigaOS/MorphOS/OpenVMS/Fuchsia/HP-UX
            'props' : ['name', 'version']
        },{
            'regex' : r'(unix) ?([\w\.]*)',                                            # UNIX
            'props' : ['name', 'version']
        }
    ]
}

# Compile all regexes
for list_ in REGEXES.values():
    for dict_ in list_:
        dict_['regex'] = re.compile( dict_['regex'], re.IGNORECASE) 


def newrgx_mapper(ua, arrays):


    if not ua: return None

    # loop through all regexes maps
    for dict_ in arrays:
        regex = dict_['regex']
        
        # try matching uastring with regexes
        matches = regex.search(ua)
        
        if matches: break
    
    if matches:

        props = dict_['props']
        
        for i, q in enumerate(props):
            
            try               : match = matches.group(i + 1)
            except IndexError : match = None

            # check if current property is actually array
            if isinstance(q, list):

                if len(q) == 2:
                    
                    if callable(q[1]):
                        # assign modified match
                        yield q[0], q[1](match) # map property q[0] to q[1](match)
                    else:
                        # assign given value, ignore regex match
                        yield q[0], q[1] # map property q[0] to q[1]
                
                elif len(q) == 3:
                    
                    # check whether function or regex
                    if callable(q[1]):
                        # call function (usually string mapper)
                        yield q[0], q[1](match, q[2]) if match else None
                    else:
                        # sanitize match using given regex
                        yield q[0], re.sub(q[1], q[2].replace('$', '\\'), match) if match else None
                elif len(q) == 4:
                    yield q[0], q[3](re.sub(q[1], q[2].replace('$', '\\'), match)) if match else None
            
            else:
                yield q, match if match else None
        




if __name__ == '__main__':

    arrays = REGEXES['browser']
    uaStrings = [
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36 Avast/99.0.15283.83',
    'Mozilla/5.0 (Windows Phone 8.1; ARM; Trident/7.0; Touch; rv:11.0; IEMobile/11.0; NOKIA; Lumia 635) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9',
    'Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.12',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/7.1.8 Safari/537.85.17',
    'Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4',
    'Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F69 Safari/600.1.4',
    'Mozilla/5.0 (Windows NT 6.1; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.6.3 (KHTML, like Gecko) Version/8.0.6 Safari/600.6.3',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.5.17 (KHTML, like Gecko) Version/8.0.5 Safari/600.5.17',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (iPad; CPU OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (X11; CrOS x86_64 7077.134.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.156 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/7.1.7 Safari/537.85.16',
    'Mozilla/5.0 (Windows NT 6.0; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Mozilla/5.0 (iPad; CPU OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B466 Safari/600.1.4',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/600.3.18 (KHTML, like Gecko) Version/8.0.3 Safari/600.3.18',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (iPad; CPU OS 8_1_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B440 Safari/600.1.4',
    'Mozilla/5.0 (Linux; U; Android 4.0.3; en-us; KFTT Build/IML74K) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36',
    'Mozilla/5.0 (iPad; CPU OS 8_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12D508 Safari/600.1.4',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Mozilla/5.0 (iPad; CPU OS 7_1_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D201 Safari/9537.53',
    'Mozilla/5.0 (Linux; U; Android 4.4.3; en-us; KFTHWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.6.3 (KHTML, like Gecko) Version/7.1.6 Safari/537.85.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/600.4.10 (KHTML, like Gecko) Version/8.0.4 Safari/600.4.10',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/7.0.6 Safari/537.78.2',
    'Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/45.0.2454.68 Mobile/12H321 Safari/600.1.4',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; rv:11.0) like Gecko',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (iPad; CPU OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B410 Safari/600.1.4',
    'Mozilla/5.0 (iPad; CPU OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B554a Safari/9537.53',
    'Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; TNJB; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; ARM; Trident/7.0; Touch; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; MDDCJS; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4',
    'Mozilla/5.0 (Linux; U; Android 4.4.3; en-us; KFASWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36',
    'Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/7.0.55539 Mobile/12H321 Safari/600.1.4',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F70 Safari/600.1.4',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; MATBJS; rv:11.0) like Gecko',
    'Mozilla/5.0 (Linux; U; Android 4.0.4; en-us; KFJWI Build/IMM76D) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36',
    'Mozilla/5.0 (iPad; CPU OS 7_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D167 Safari/9537.53',
    'Mozilla/5.0 (X11; CrOS armv7l 7077.134.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.156 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/600.2.5 (KHTML, like Gecko) Version/8.0.2 Safari/600.2.5',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0'
    ]

    out = []
    ii = 0
    for ua in uaStrings:
        ii += 1

        test_dict = test(ua)

        for key, value in newrgx_mapper(ua, arrays):
            out.append(value == test_dict[key])



    print(ii, all(out))
            


