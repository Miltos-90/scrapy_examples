""" TESTING VARIOUS STUFF: https://whatmyuseragent.com/platforms

"""

import re
from parser_utils import str_mapper, trim, lowerize # fix these
from parser_utils import EMPTY
from typing import Callable, Union

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

wtf = {
    'browser': [
        {   
            'regex' : r'\b(?:crmo|crios)\/([\w\.]+)',                         # Chrome for Android/iOS
            'props' : {'version': None, 'name': 'Chrome'}
        },{ 
            'regex' : r'edg(?:e|ios|a)?\/([\w\.]+)',                          # Microsoft Edge
            'props' : {'version': None, 'name': 'Edge'}
        },{ 
            'regex' : r'(opera mini)\/([-\w\.]+)',                            # Opera Mini
            'props' : {'name': None, 'version': None}
        },{
            'regex' : r'(opera [mobiletab]{3,6})\b.+version\/([-\w\.]+)',     # Opera Mobi/Tablet
            'props' : {'name': None, 'version': None}
        },{
            'regex' : r'(opera)(?:.+version\/|[\/ ]+)([\w\.]+)',              # Opera
            'props' : {'name': None, 'version': None}
        },{ 
            'regex' : r'opios[\/ ]+([\w\.]+)',                              # Opera mini on iphone >= 8.0
            'props' : {'version': None, 'name': 'Opera Mini'}
        },{ 
            'regex' : r'\bopr\/([\w\.]+)',                                  # Opera Webkit
            'props' : {'version': None, 'name': 'Opera'}
        },{ 
            'regex' : r'(kindle)\/([\w\.]+)',                                 # Kindle
            'props' : {'name': None, 'version': None}
        },{
            'regex' : r'(lunascape|maxthon|netfront|jasmine|blazer)[\/ ]?([\w\.]*)',  # Lunascape/Maxthon/Netfront/Jasmine/Blazer
            'props' : {'name': None, 'version': None}
        },{ 
            'regex' : r'(avant |iemobile|slim)(?:browser)?[\/ ]?([\w\.]*)',           # Avant/IEMobile/SlimBrowser
            'props' : {'name': None, 'version': None}
        },{
            'regex' : r'(ba?idubrowser)[\/ ]?([\w\.]+)',                              # Baidu Browser
            'props' : {'name': None, 'version': None}
        },{ 
            'regex' : r'(?:ms|\()(ie) ([\w\.]+)',                                     # Internet Explorer
            'props' : {'name': None, 'version': None}
        },{ 
            'regex' : r'(flock|rockmelt|midori|epiphany|silk|skyfire|ovibrowser|bolt|iron|vivaldi|iridium|phantomjs|bowser|quark|qupzilla|falkon|rekonq|puffin|brave|whale|qqbrowserlite|qq)\/([-\w\.]+)',  # Rekonq/Puffin/Brave/Whale/QQBrowserLite/QQ, aka ShouQ
            'props' : {'name': None, 'version': None}
        },{ 
            'regex' : r'(weibo)__([\d\.]+)',                                   # Weibo
            'props' : {'name': None, 'version': None}
        },{
            'regex' : r'(?:\buc? ?browser|(?:juc.+)ucweb)[\/ ]?([\w\.]+)',    # UCBrowser
            'props' : {'version': None, 'name': 'UCBrowser'}, 
        },{
            'regex' : r'\bqbcore\/([\w\.]+)',                                 # WeChat Desktop for Windows Built-in Browser
            'props' : {'version': None, 'name': 'WeChat(Win) Desktop'}, 
        },{
            'regex' : r'micromessenger\/([\w\.]+)',                           # WeChat
            'props' : {'version': None, 'name': 'WeChat'}, 
        },{
            'regex' : r'konqueror\/([\w\.]+)',                                # Konqueror
            'props' : {'version': None, 'name': 'Konqueror'}, 
        },{
            'regex' : r'trident.+rv[: ]([\w\.]{1,9})\b.+like gecko',          # IE11
            'props' : {'version': None, 'name': 'IE'} 
        },{
            'regex' : r'yabrowser\/([\w\.]+)',                                # Yandex
            'props' : {'version': None, 'name': 'Yandex'}, 
        },{
            'regex' : r'(avast|avg)\/([\w\.]+)',                              # Avast/AVG Secure Browser
            'props' : {
                'name'   : lambda s: re.sub(r'(.+)', '\\1 Secure Browser', s),
                'version': None
                }
        },{
            'regex' : r'\bfocus\/([\w\.]+)',                                  # Firefox Focus
            'props' : {'version': None, 'name': 'Firefox Focus'}, 
        },{
            'regex' : r'\bopt\/([\w\.]+)',                                    # Opera Touch
            'props' : {'version': None, 'name': 'Opera Touch'}, 
        },{
            'regex' :  r'coc_coc\w+\/([\w\.]+)',                              # Coc Coc Browser 
            'props' : {'version': None, 'name': 'Coc Coc'},
        },{
            'regex' : r'dolfin\/([\w\.]+)',                                   # Dolphin
            'props' : {'version': None, 'name': 'Dolphin'}, 
        },{
            'regex' : r'coast\/([\w\.]+)',                                    # Opera Coast
            'props' : {'version': None, 'name': 'Opera Coast'}, 
        },{
            'regex' : r'miuibrowser\/([\w\.]+)',                              # MIUI Browser
            'props' : {'version': None, 'name': 'MIUI Browser'}, 
        },{
            'regex' : r'fxios\/([-\w\.]+)',                                   # Firefox for iOS
            'props' : {'version': None, 'name': 'Firefox'}, 
        },{
            'regex' : r'\bqihu|(qi?ho?o?|360)browser',                        # 360
            'props' : {'name': '360 Browser'},  
        },{ 
            'regex' : r'(oculus|samsung|sailfish)browser\/([\w\.]+)',         # Oculus/Samsung/Sailfish Browser 
            'props' : {
                'name'   : lambda s: re.sub(r'(.+)', '\\1 Browser', s),
                'version': None
                },
        },{
            'regex' : r'(comodo_dragon)\/([\w\.]+)',                          # Comodo Dragon
            'props' : {
                'name'   : lambda s: re.sub(r'_', ' ', s), 
                'version': None
                }, 
        },{
            'regex' : r'(electron)\/([\w\.]+) safari',                                # Electron-based App
            'props' : {'name': None, 'version': None}
        },{
            'regex' : r'(tesla)(?: qtcarbrowser|\/(20\d\d\.[-\w\.]+))',               # Tesla
            'props' : {'name': None, 'version': None}
        },{
            'regex' : r'm?(qqbrowser|baiduboxapp|2345Explorer)[\/ ]?([\w\.]+)',        # QQBrowser/Baidu App/2345 Browser
            'props' : {'name': None, 'version': None}
        },{
            'regex' : r'(metasr)[\/ ]?([\w\.]+)',                                     # SouGouBrowser
            'props' : {'name': None} 
        },{
            'regex' : r'(lbbrowser)',                                                  # LieBao Browser
            'props' : {'name': None, 'version': None}, 
        },{
            'regex' : r'((?:fban\/fbios|fb_iab\/fb4a)(?!.+fbav)|;fbav\/([\w\.]+);)', # Facebook App for iOS & Android
            'props' : {'name': 'Facebook', 'version': None},                        
        },{
            'regex' : r'safari (line)\/([\w\.]+)',                             # Line App for iOS
            'props' : {'name': None, 'version': None}, 
        },{
            'regex' : r'\b(line)\/([\w\.]+)\/iab',                                        # Line App for Android
            'props' : {'name': None, 'version': None}, 
        },{
            'regex' : r'(chromium|instagram)[\/ ]([-\w\.]+)',                              # Chromium/Instagram
            'props' : {'name': None, 'version': None}, 
        },{
            'regex' : r'\bgsa\/([\w\.]+) .*safari\/',                           # Google Search Appliance on iOS
            'props' : {'version': None, 'name': 'GSA'},                             
        },{
            'regex' : r'headlesschrome(?:\/([\w\.]+)| )',                           # Chrome Headless
            'props' : {'version': None, 'name': 'Chrome Headless'},            
        },{
            'regex' : r' wv\).+(chrome)\/([\w\.]+)',                                # Chrome WebView
            'props' : {'name': 'Chrome WebView', 'version': None},             
        },{
            'regex' : r'droid.+ version\/([\w\.]+)\b.+(?:mobile safari|safari)',    # Android Browser
            'props' : {'version': None, 'name': 'Android Browser'},            
        },{
            'regex' : r'(chrome|omniweb|arora|[tizenoka]{5} ?browser)\/v?([\w\.]+)',  # Chrome/OmniWeb/Arora/Tizen/Nokia
            'props' : {'name': None, 'version': None},                                      
        },{
            'regex' : r'version\/([\w\.]+) .*mobile\/\w+ (safari)',                     # Mobile Safari
            'props' : {'version': None, 'name': 'Mobile Safari'},                   
        },{
            'regex' : r'version\/([\w\.]+) .*(mobile ?safari|safari)',                  # Safari & Safari Mobile
            'props' : {'version': None, 'name': None},                                      
        },{
            'regex' : r'webkit.+?(mobile ?safari|safari)(\/[\w\.]+)',                   # Safari < 3.0 
            'props' : {
                'name'   : None,                                                           
                'version': lambda s: str_mapper(s, OLD_SAFARI_MAP)
                },        
        },{
            'regex' : r'(webkit|khtml)\/([\w\.]+)', 
            'props' : {'name': None, 'version': None}, 
        },{
            'regex' : r'(navigator|netscape\d?)\/([-\w\.]+)',                           # Netscape 
            'props' : {'name': 'Netscape', 'version': None},
        },{
            'regex' : r'mobile vr; rv:([\w\.]+)\).+firefox',                            # Firefox Reality
            'props' : {'version': None, 'name': 'Firefox Reality'},            
        },{
            'regex' : r'ekiohf.+(flow)\/([\w\.]+)',                                   # Flow
            'props' : {'name': None, 'version': None}
        },{
            'regex' : r'(swiftfox)',                                                  # Swiftfox
            'props' : {'name': None, 'version': None}
        },{
            'regex' : r'(icedragon|iceweasel|camino|chimera|fennec|maemo browser|minimo|conkeror|klar)[\/ ]?([\w\.\+]+)',                         # IceDragon/Iceweasel/Camino/Chimera/Fennec/Maemo/Minimo/Conkeror/Klar
            'props' : {'name': None, 'version': None}
        },{
            'regex' : r'(seamonkey|k-meleon|icecat|iceape|firebird|phoenix|palemoon|basilisk|waterfox)\/([-\w\.]+)$',                             # Firefox/SeaMonkey/K-Meleon/IceCat/IceApe/Firebird/Phoenix
            'props' : {'name': None, 'version': None}
        },{
            'regex' : r'(firefox)\/([\w\.]+)',                                        # Other Firefox-based
            'props' : {'name': None, 'version': None}
        },{
            'regex' : r'(mozilla)\/([\w\.]+) .+rv\:.+gecko\/\d+',                     # Mozilla
            'props' : {'name': None, 'version': None}
        },{
            'regex' : r'(polaris|lynx|dillo|icab|doris|amaya|w3m|netsurf|sleipnir|obigo|mosaic|(?:go|ice|up)[\. ]?browser)[-\/ ]?v?([\w\.]+)',    # Polaris/Lynx/Dillo/iCab/Doris/Amaya/w3m/NetSurf/Sleipnir/Obigo/Mosaic/Go/ICE/UP.Browser
            'props' : {'name': None, 'version': None}
        },{
            'regex' : r'(links) \(([\w\.]+)',                                          # Links
            'props' : {'name': None, 'version': None}
        }
    ],

    'cpu': [
        {
            'regex' : r'(?:(amd|x(?:(?:86|64)[-_])?|wow|win)64)[;\)]',        # AMD64 (x64)
            'props' : {'architecture': 'amd64'},                              
        },{
            'regex' : r'(ia32(?=;))',                                         # IA32 (quicktime)
            'props' : {'architecture': lambda s: s.lower()},                       
        },{
            'regex' : r'((?:i[346]|x)86)[;\)]',                               # IA32 (x86)
            'props' : {'architecture', 'ia32'}, 
        },{
            'regex' : r'\b(aarch64|arm(v?8e?l?|_?64))\b',                     # ARM64
            'props' : {'architecture': 'arm64'}, 
        },{
            'regex' : r'\b(arm(?:v[67])?ht?n?[fl]p?)\b',                      # ARMHF
            'props' : {'architecture': 'armhf'}, 
        },{
            'regex' : r'windows (ce|mobile); ppc;',                           # PocketPC mistakenly identified as PowerPC
            'props' : {'architecture': 'arm'},  
        },{
            'regex' : r'((?:ppc|powerpc)(?:64)?)(?: mac|;|\))',               # PowerPC
            'props' : {'architecture': lambda s: re.sub(r'ower', EMPTY, s).lower()},
        },{
            'regex' : r'(sun4\w)[;\)]',                                       # SPARC
            'props' : {'architecture': 'sparc'}, 
        },{
            'regex' : r'((?:avr32|ia64(?=;))|68k(?=\))|\barm(?=v(?:[1-7]|[5-7]1)l?|;|eabi)|(?=atmel )avr|(?:irix|mips|sparc)(?:64)?\b|pa-risc)',  
            'props' : {'architecture': lambda s: s.lower()}                              # IA64, 68K, ARM/64, AVR/32, IRIX/64, MIPS/64, SPARC/64, PA-RISC
        }
    ], 

    'device': [
        {
            'regex' : r'\b(sch-i[89]0\d|shw-m380s|sm-[pt]\w{2,4}|gt-[pn]\d{2,4}|sgh-t8[56]9|nexus 10)',   # Samsung devices 
            'props' : {'model': None, 'vendor': 'Samsung', 'type': 'tablet'}, 
        },{
            'regex' : r'\b((?:s[cgp]h|gt|sm)-\w+|galaxy nexus)', 
            'props' : {'model': None, 'vendor': 'Samsung', 'type': 'mobile'}, 
            },{
            'regex' : r'samsung[- ]([-\w]+)', 
            'props' : {'model': None, 'vendor': 'Samsung', 'type': 'mobile'},  
            },{
            'regex' : r'sec-(sgh\w+)', 
            'props' : {'model': None, 'vendor': 'Samsung', 'type': 'mobile'}, 
        },{
            'regex' : r'\((ip(?:hone|od)[\w ]*);',                                    # iPod/iPhone
            'props' : {'model': None, 'vendor': 'Apple', 'type': 'mobile'}, 
        },{
            'regex' : r'\((ipad);[-\w\),; ]+apple',                                           # iPad
            'props' : {'model': None, 'vendor': 'Apple', 'type': 'tablet'}, 
        },{
            'regex' : r'applecoremedia\/[\w\.]+ \((ipad)', 
            'props' : {'model': None, 'vendor': 'Apple', 'type': 'tablet'}, 
        },{
            'regex' : r'\b(ipad)\d\d?,\d\d?[;\]].+ios', 
            'props' : {'model': None, 'vendor': 'Apple', 'type': 'tablet'}, 
        },{
            'regex' : r'\b((?:ag[rs][23]?|bah2?|sht?|btv)-a?[lw]\d{2})\b(?!.+d\/s)',  # Huawei
            'props' : {'model': None, 'vendor': 'Huawei', 'type': 'tablet'}, 
        },{
            'regex' : r'(?:huawei|honor)([-\w ]+)[;\)]', 
            'props' : {'model': None, 'vendor': 'Apple', 'type': 'tablet'}, 
        },{
            'regex' : r'\b(nexus 6p|\w{2,4}-[atu]?[ln][01259x][012359][an]?)\b(?!.+d\/s)', 
            'props' : {'model': None, 'vendor': 'Apple', 'type': 'mobile'}, 
        },{
            'regex' : r'\b(poco[\w ]+)(?: bui|\))',                                           # Xiaomi POCO
            'props' : {
                'model'  : lambda s: re.sub('_', ' ', s), 
                'vendor' : 'Xiaomi', 
                'type'   : 'mobile'
                }, 
        },{
            'regex' : r'\b; (\w+) build\/hm\1',                                               # Xiaomi Hongmi 'numeric' models
            'props' : {
                'model'  : lambda s: re.sub('_', ' ', s), 
                'vendor' : 'Xiaomi', 
                'type'   : 'mobile'
                }, 
        },{
            'regex' : r'\b(hm[-_ ]?note?[_ ]?(?:\d\w)?) bui',                                 # Xiaomi Hongmi
            'props' : {
                'model'  : lambda s: re.sub('_', ' ', s), 
                'vendor' : 'Xiaomi', 
                'type'   : 'mobile'
                }, 
        },{
            'regex' : r'\b(redmi[\-_ ]?(?:note|k)?[\w_ ]+)(?: bui|\))',                       # Xiaomi Redmi
            'props' : {
                'model'  : lambda s: re.sub('_', ' ', s), 
                'vendor' : 'Xiaomi', 
                'type'   : 'mobile'
                }, 
        },{
            'regex' : r'\b(mi[-_ ]?(?:a\d|one|one[_ ]plus|note lte|max)?[_ ]?(?:\d?\w?)[_ ]?(?:plus|se|lite)?)(?: bui|\))',  # Xiaomi Mi
            'props' : {
                'model'  : lambda s: re.sub('_', ' ', s), 
                'vendor' : 'Xiaomi', 
                'type'   : 'mobile'
                }, 
        },{
            'regex' : r'\b(mi[-_ ]?(?:pad)(?:[\w_ ]+))(?: bui|\))',                   # Mi Pad tablets
            'props' : {
                'model'  : lambda s: re.sub('_', ' ', s), 
                'vendor' : 'Xiaomi', 
                'type'   : 'tablet'
                }, 
        },{
            'regex' : r'; (\w+) bui.+ oppo',                                                  # OPPO
            'props' : {'model': None, 'vendor': 'OPPO', 'type': 'mobile'}
        },{
            'regex' : r'\b(cph[12]\d{3}|p(?:af|c[al]|d\w|e[ar])[mt]\d0|x9007|a101op)\b', 
            'props' : {'model': None, 'vendor': 'OPPO', 'type': 'mobile'}
        },{
            'regex' : r'vivo (\w+)(?: bui|\))',                                               # Vivo
            'props' : {'model': None, 'vendor': 'Vivo', 'type': 'mobile'}
        },{ 
            'regex' : r'\b(v[12]\d{3}\w?[at])(?: bui|;)',
            'props' : {'model': None, 'vendor': 'Vivo', 'type': 'mobile'}
        },{
            'regex' : r'\b(rmx[12]\d{3})(?: bui|;|\))',                               # Realme
            'props' : {'model': None, 'vendor': 'Realme', 'type': 'mobile'}
        },{
            'regex' : r'\b(milestone|droid(?:[2-4x]| (?:bionic|x2|pro|razr))?:?( 4g)?)\b[\w ]+build\/', # Motorola
            'props' : {'model': None, 'vendor': 'Motorola', 'type': 'mobile'}, 
        },{ 
            'regex' : r'\bmot(?:orola)?[- ](\w*)',
            'props' : {'model': None, 'vendor': 'Motorola', 'type': 'mobile'}, 
        },{ 
            'regex' : r'((?:moto[\w\(\) ]+|xt\d{3,4}|nexus 6)(?= bui|\)))',
            'props' : {'model': None, 'vendor': 'Motorola', 'type': 'mobile'}, 
        },{
            'regex' : r'\b(mz60\d|xoom[2 ]{0,2}) build\/', 
            'props' : {'model': None, 'vendor': 'Motorola', 'type': 'tablet'},  
        },{
            'regex' : r'((?=lg)?[vl]k\-?\d{3}) bui| 3\.[-\w; ]{10}lg?-([06cv9]{3,4})', # 'LG'
            'props' : {'model': None, 'vendor': 'LG', 'type': 'tablet'},  
        },{
            'regex' : r'(lm(?:-?f100[nv]?|-[\w\.]+)(?= bui|\))|nexus [45])',
            'props' : {'model': None, 'vendor': 'LG', 'type': 'mobile'},  
        },{
            'regex' : r'\blg[-e;\/ ]+((?!browser|netcast|android tv)\w+)',
            'props' : {'model': None, 'vendor': 'LG', 'type': 'mobile'},  
        },{
            'regex' : r'\blg-?([\d\w]+) bui', 
            'props' : {'model': None, 'vendor': 'LG', 'type': 'mobile'},  
        },{
            'regex' : r'(ideatab[-\w ]+)',                                                    # Lenovo 
            'props' : {'model': None, 'vendor': 'Lenovo', 'type': 'tablet'},  
        },{
            'regex' : r'lenovo ?(s[56]000[-\w]+|tab(?:[\w ]+)|yt[-\d\w]{6}|tb[-\d\w]{6})', 
            'props' : {'model': None, 'vendor': 'Lenovo', 'type': 'tablet'},  
        },{
            'regex' : r'(?:maemo|nokia).*(n900|lumia \d+)',                                   # Nokia
            'props' : {
                'model'  : lambda s: re.sub('_', ' ', s), 
                'vendor' : 'Nokia', 
                'type'   : 'mobile'
                }, 
        },{
            'regex' : r'nokia[-_ ]?([-\w\.]*)', 
            'props' : {
                'model'  : lambda s: re.sub('_', ' ', s), 
                'vendor' : 'Nokia', 
                'type'   : 'mobile'
                }, 
        },{
            'regex' : r'(pixel c)\b',                                                 # Google Pixel C
            'props' : {'model': None, 'vendor': 'Google', 'type': 'tablet'},
        },{
            'regex' : r'droid.+; (pixel[\daxl ]{0,6})(?: bui|\))',                    # Google Pixel
            'props' : {'model': None, 'vendor': 'Google', 'type': 'mobile'},
        },{
            'regex' : r'droid.+ ([c-g]\d{4}|so[-gl]\w+|xq-a\w[4-7][12])(?= bui|\).+chrome\/(?![1-6]{0,1}\d\.))', # Sony
            'props' : {'model': None, 'vendor': 'Sony', 'type': 'mobile'},
        },{
            'regex' : r'sony tablet [ps]', 
            'props' : {'model': 'Xperia Tablet', 'vendor': 'Sony', 'type': 'tablet'}, 
        },{
            'regex' : r'\b(?:sony)?sgp\w+(?: bui|\))', 
            'props' : {'model': 'Xperia Tablet', 'vendor': 'Sony', 'type': 'tablet'}, 
        },{
            'regex' : r' (kb2005|in20[12]5|be20[12][59])\b',                                  # OnePlus
            'props' : {'model': None, 'vendor': 'OnePlus', 'type': 'mobile'}, 
        },{
            'regex' : r'(?:one)?(?:plus)? (a\d0\d\d)(?: b|\))', 
            'props' : {'model': None, 'vendor': 'OnePlus', 'type': 'mobile'}, 
        },{
            'regex' : r'(alexa)webm',                                                         # Amazon
            'props' : {'model': None, 'vendor': 'Amazon', 'type': 'tablet'}, 
        },{
            'regex' : r'(kf[a-z]{2}wi)( bui|\))',                                             # Kindle Fire without Silk
            'props' : {'model': None, 'vendor': 'Amazon', 'type': 'tablet'}, 
        },{
            'regex' : r'(kf[a-z]+)( bui|\)).+silk\/',                                          # Kindle Fire HD
            'props' : {'model': None, 'vendor': 'Amazon', 'type': 'tablet'}, 
        },{
            'regex' : r'((?:sd|kf)[0349hijorstuw]+)( bui|\)).+silk\/',                # Fire Phone
            'props' : {
                'model'  : lambda s: re.sub(r'(.+)', 'Fire Phone \\1', s), 
                'vendor' : 'Amazon', 
                'type'   : 'mobile'
                }, 
        },{
            'regex' : r'(playbook);[-\w\),; ]+(rim)',                                 # BlackBerry PlayBook
            'props' : {'model': None, 'vendor' : None, 'type': 'tablet'},
        },{
            'regex' : r'\b((?:bb[a-f]|st[hv])100-\d)',                                    # BlackBerry 10
            'props' : {'model': None, 'vendor': 'BlackBerry', 'type': 'mobile'}, 
        },{
            'regex' : r'\(bb10; (\w+)',                                                        # BlackBerry 10
            'props' : {'model': None, 'vendor': 'BlackBerry', 'type': 'mobile'}, 
        },{
            'regex' : r'(?:\b|asus_)(transfo[prime ]{4,10} \w+|eeepc|slider \w+|nexus 7|padfone|p00[cj])', # Asus
            'props' : {'model': None, 'vendor': 'ASUS', 'type': 'tablet'}, 
        },{
            'regex' : r' (z[bes]6[027][012][km][ls]|zenfone \d\w?)\b', 
            'props' : {'model': None, 'vendor': 'ASUS', 'type': 'mobile'}, 
        },{
            'regex' : r'(nexus 9)',                                                   # HTC Nexus 9
            'props' : {'model': None, 'vendor': 'HTC', 'type': 'tablet'}, 
        },{
            'regex' : r'(htc)[-;_ ]{1,2}([\w ]+(?=\)| bui)|\w+)',                             # HTC
            'props' : {
                'vendor': None, 
                'model' : lambda s: re.sub('_', ' ', s), 
                'type'  : 'mobile'
                },
        },{
            'regex' : r'(zte)[- ]([\w ]+?)(?: bui|\/|\))',                                    # ZTE
            'props' : {
                'vendor': None, 
                'model' : lambda s: re.sub('_', ' ', s),
                'type'  : 'mobile'}
        },{
            'regex' : r'(alcatel|geeksphone|nexian|panasonic|sony)[-_ ]?([-\w]*)',             # Alcatel/GeeksPhone/Nexian/Panasonic/Sony
            'props' : {
                'vendor': None, 
                'model' : lambda s: re.sub('_', ' ', s),
                'type'  : 'mobile'}
        },{
            'regex' : r'droid.+; ([ab][1-7]-?[0178a]\d\d?)',                          # Acer
            'props' : {'model': None, 'vendor': 'Acer', 'type': 'tablet'}, 

        },{
            'regex' : r'\bmz-([-\w]{2,})',                                          # Meizu
            'props' : {'model': None, 'vendor': 'Meizu', 'type': 'mobile'}, 
        },{
            'regex' : r'droid.+; (m[1-5] note) bui',                                # Meizu
            'props' : {'model': None, 'vendor': 'Meizu', 'type': 'mobile'}, 
        },{
            'regex' : r'\b(sh-?[altvz]?\d\d[a-ekm]?)',                                # Sharp
            'props' : {'model': None, 'vendor': 'Sharp', 'type': 'mobile'}, 
        },{
            'regex' : r'(blackberry|benq|palm(?=\-)|sonyericsson|acer|asus|dell|meizu|motorola|polytron)[-_ ]?([-\w]*)',  # BlackBerry/BenQ/Palm/Sony-Ericsson/Acer/Asus/Dell/Meizu/Motorola/Polytron
            'props' : {'vendor': None, 'model': None, 'type': 'mobile'}, 
        },{
            'regex' : r'(hp) ([\w ]+\w)',                                                     # HP iPAQ
            'props' : {'vendor': None, 'model': None, 'type': 'mobile'},  
        },{ 
            'regex' : r'(asus)-?(\w+)',                                                       # Asus
            'props' : {'vendor': None, 'model': None, 'type': 'mobile'}, 
        },{
            'regex' : r'(microsoft); (lumia[\w ]+)',                                          # Microsoft Lumia
            'props' : {'vendor': None, 'model': None, 'type': 'mobile'}, 
        },{
            'regex' : r'(lenovo)[-_ ]?([-\w]+)',                                              # Lenovo
            'props' : {'vendor': None, 'model': None, 'type': 'mobile'}, 
        },{
            'regex' : r'(jolla)',                                                             # Jolla
            'props' : {'vendor': None, 'model': None, 'type': 'mobile'}, 
        },{
            'regex' : r'(oppo) ?([\w ]+) bui',                                                 # OPPO
            'props' : {'vendor': None, 'model': None, 'type': 'mobile'}, 
        },{
            'regex' : r'(archos) (gamepad2?)',                                                # Archos
            'props' : {'vendor': None, 'model': None, 'type': 'tablet'}, 
        },{
            'regex' : r'(hp).+(touchpad(?!.+tablet)|tablet)',                                 # HP TouchPad
            'props' : {'vendor': None, 'model': None, 'type': 'tablet'}, 
        },{
            'regex' : r'(kindle)\/([\w\.]+)',                                                 # Kindle
            'props' : {'vendor': None, 'model': None, 'type': 'tablet'}, 
        },{ 
            'regex' : r'(nook)[\w ]+build\/(\w+)',                                            # Nook
            'props' : {'vendor': None, 'model': None, 'type': 'tablet'}, 
        },{
            'regex' : r'(dell) (strea[kpr\d ]*[\dko])',                                       # Dell Streak
            'props' : {'vendor': None, 'model': None, 'type': 'tablet'}, 
        },{
            'regex' : r'(le[- ]+pan)[- ]+(\w{1,9}) bui',                                      # Le Pan Tablets
            'props' : {'vendor': None, 'model': None, 'type': 'tablet'}, 
        },{ 
            'regex' : r'(trinity)[- ]*(t\d{3}) bui',                                          # Trinity Tablets
            'props' : {'vendor': None, 'model': None, 'type': 'tablet'}, 
        },{
            'regex' : r'(gigaset)[- ]+(q\w{1,9}) bui',                                        # Gigaset Tablets
            'props' : {'vendor': None, 'model': None, 'type': 'tablet'}, 
        },{ 
            'regex' : r'(vodafone) ([\w ]+)(?:\)| bui)',                                       # Vodafone
            'props' : {'vendor': None, 'model': None, 'type': 'tablet'}, 
        },{
            'regex' : r'(surface duo)',                                               # Surface Duo
            'props' : {'model': None, 'vendor': 'Microsoft', 'type': 'tablet'}, 
        },{
            'regex' : r'droid [\d\.]+; (fp\du?)(?: b|\))',                            # Fairphone
            'props' : {'model': None, 'vendor': 'Fairphone', 'type': 'mobile'}, 
        },{
            'regex' : r'(u304aa)',                                                    # AT&T
            'props' : {'model': None, 'vendor': 'AT&T', 'type': 'mobile'},  
        },{
            'regex' : r'\bsie-(\w*)',                                                 # Siemens
            'props' : {'model': None, 'vendor': 'Siemens', 'type': 'mobile'}, 
        },{
            'regex' : r'\b(rct\w+) b',                                                # RCA Tablets
            'props' : {'model': None, 'vendor': 'RCA', 'type': 'tablet'}, 
        },{
            'regex' : r'\b(venue[\d ]{2,7}) b',                                       # Dell Venue Tablets
            'props' : {'model': None, 'vendor': 'Dell', 'type': 'tablet'}, 
        },{
            'regex' : r'\b(q(?:mv|ta)\w+) b',                                         # Verizon Tablet
            'props' : {'model': None, 'vendor': 'Verizon', 'type': 'tablet'}, 
        },{
            'regex' : r'\b(?:barnes[& ]+noble |bn[rt])([\w\+ ]*) b',                  # Barnes & Noble Tablet
            'props' : {'model': None, 'vendor': 'Barnes & Noble', 'type': 'tablet'}, 
        },{
            'regex' : r'\b(tm\d{3}\w+) b',
            'props' : {'model': None, 'vendor': 'NuVision', 'type': 'tablet'}, 
        },{
            'regex' : r'\b(k88) b',                                                   # ZTE K Series Tablet
            'props' : {'model': None, 'vendor': 'ZTE', 'type': 'tablet'}, 
        },{
            'regex' : r'\b(nx\d{3}j) b',                                              # ZTE Nubia
            'props' : {'model': None, 'vendor': 'ZTE', 'type': 'mobile'},  
        },{
            'regex' : r'\b(gen\d{3}) b.+49h',                                         # Swiss GEN Mobile
            'props' : {'model': None, 'vendor': 'Swiss', 'type': 'mobile'},  
        },{
            'regex' : r'\b(zur\d{3}) b',                                              # Swiss ZUR Tablet
            'props' : {'model': None, 'vendor': 'Swiss', 'type': 'tablet'}, 
        },{
            'regex' : r'\b((zeki)?tb.*\b) b',                                         # Zeki Tablets
            'props' : {'model': None, 'vendor': 'Zeki', 'type': 'tablet'}, 
        },{
            'regex' : r'\b([yr]\d{2}) b',                                             # Dragon Touch Tablet
            'props' : {'vendor': 'Dragon Touch', 'model': None, 'type': 'tablet'}, 
        },{
            'regex' : r'\b(dragon[- ]+touch |dt)(\w{5}) b',                           # Dragon Touch Tablet
            'props' : {'vendor': 'Dragon Touch', 'model': None, 'type': 'tablet'}, 
        },{
            'regex' : r'\b(ns-?\w{0,9}) b',                                           # Insignia Tablets
            'props' : {'model': None, 'vendor': 'Insignia', 'type': 'tablet'}, 
        },{
            'regex' : r'\b((nxa|next)-?\w{0,9}) b',                                   # NextBook Tablets
            'props' : {'model': None, 'vendor': 'NextBook', 'type': 'tablet'}, 
        },{
            'regex' : r'\b(xtreme\_)?(v(1[045]|2[015]|[3469]0|7[05])) b',             # Voice Xtreme Phones
            'props' : {'vendor': 'Voice', 'model': None, 'type': 'mobile'}, 
        },{
            'regex' : r'\b(lvtel\-)?(v1[12]) b',                                      # LvTel Phones
            'props' : {'vendor': 'LvTel', 'model': None, 'type': 'mobile'}, 
        },{
            'regex' : r'\b(ph-1) ',                                                   # Essential PH-1
            'props' : {'model': None, 'vendor': 'Essential', 'type': 'mobile'}, 
        },{
            'regex' : r'\b(v(100md|700na|7011|917g).*\b) b',                          # Envizen Tablets
            'props' : {'model': None, 'vendor': 'Envizen', 'type': 'tablet'}, 
        },{
            'regex' : r'\b(trio[-\w\. ]+) b',                                         # MachSpeed Tablets
            'props' : {'model': None, 'vendor': 'MachSpeed', 'type': 'tablet'}, 
        },{
            'regex' : r'\btu_(1491) b',                                               # Rotor Tablets
            'props' : {'model': None, 'vendor': 'Rotor', 'type': 'tablet'}, 
        },{
            'regex' : r'(shield[\w ]+) b',                                            # Nvidia Shield Tablets
            'props' : {'model': None, 'vendor': 'Nvidia', 'type': 'tablet'}, 
        },{
            'regex' : r'(sprint) (\w+)',                                              # Sprint Phones
            'props' : {'vendor': None, 'model': None, 'type': 'mobile'}, 
        },{
            'regex' : r'(kin\.[onetw]{3})',                                           # Microsoft Kin
            'props' : {
                'model' : lambda s: re.sub(r'\.', ' ', s),
                'vendor': 'Microsoft',
                'type'  : 'mobile'}
        },{
            'regex' : r'droid.+; (cc6666?|et5[16]|mc[239][23]x?|vc8[03]x?)\)',        # Zebra
            'props' : {'model': None, 'vendor': 'Zebra', 'type': 'tablet'}, 
        },{
            'regex' : r'droid.+; (ec30|ps20|tc[2-8]\d[kx])\)', 
            'props' : {'model': None, 'vendor': 'Zebra', 'type': 'mobile'}, 
        },{
            'regex' : r'(ouya)',                                                              # Ouya
            'props' : {'vendor': None, 'model': None, 'type': 'console'},  
        },{
            'regex' : r'(nintendo) ([wids3utch]+)',                                          # Nintendo
            'props' : {'vendor': None, 'model': None, 'type': 'console'},  
        },{
            'regex' : r'droid.+; (shield) bui',                                       # Nvidia
            'props' : {'model': None, 'vendor': 'Nvidia', 'type': 'console'}, 
        },{
            'regex' : r'(playstation [345portablevi]+)',                              # Playstation
            'props' : {'model': None, 'vendor': 'Sony', 'type': 'console'}, 
        },{
            'regex' : r'\b(xbox(?: one)?(?!; xbox))[\); ]',                           # Microsoft Xbox
            'props' : {'model': None, 'vendor': 'Microsoft', 'type': 'console'},  
        },{
            'regex' : r'smart-tv.+(samsung)',                                         # Samsung SmartTV
            'props' : {'vendor': None, 'type': 'smarttv'}, 
        },{
            'regex' : r'hbbtv.+maple;(\d+)',
            'props' : {
                'model' : lambda s: re.sub(r'^', 'SmartTV', s),
                'vendor': 'Samsung',
                'type'  : 'smarttv'}
        },{
            'regex' : r'(nux; netcast.+smarttv|lg (netcast\.tv-201\d|android tv))',   # 'LG' SmartTV
            'props' : {'vendor': 'LG', 'type': 'smarttv'},  
        },{
            'regex' : r'(apple) ?tv',                                                 # Apple TV
            'props' : {'vendor': None, 'model': 'Apple TV', 'type': 'smarttv'},  
        },{
            'regex' : r'crkey',                                                       # Google Chromecast
            'props' : {'model': 'Chromecast', 'vendor': 'Google', 'type': 'smarttv'},  
        },{
            'regex' : r'droid.+aft(\w)( bui|\))',                                     # Fire TV
            'props' : {'model': None, 'vendor': 'Amazon', 'type': 'smarttv'},  
        },{
            'regex' : r'\(dtv[\);].+(aquos)',                                         # Sharp
            'props' : {'model': None, 'vendor': 'Sharp', 'type': 'smarttv'},  
        },{
            #re.sub(r'\s\s*$', EMPTY, re.sub(r'^\s\s*', EMPTY, string))
            'regex' : r'\b(roku)[\dx]*[\)\/]((?:dvp-)?[\d\.]*)',                              # Roku
            'props' : {
                'vendor': lambda s: re.sub(r'\s\s*$', EMPTY, re.sub(r'^\s\s*', EMPTY, s)), 
                'model' : lambda s: re.sub(r'\s\s*$', EMPTY, re.sub(r'^\s\s*', EMPTY, s)),  
                'type'  : 'smarttv'},  
        },{
            'regex' : r'hbbtv\/\d+\.\d+\.\d+ +\([\w ]*; *(\w[^;]*);([^;]*)',                   # HbbTV devices
            'props' : {
                'vendor': lambda s: re.sub(r'\s\s*$', EMPTY, re.sub(r'^\s\s*', EMPTY, s)), 
                'model' : lambda s: re.sub(r'\s\s*$', EMPTY, re.sub(r'^\s\s*', EMPTY, s)), 
                'type'  : 'smarttv'
                },  
        },{
            'regex' : r'\b(android tv|smart[- ]?tv|opera tv|tv; rv:)\b',              # SmartTV from Unidentified Vendors
            'props' : {'type': 'smarttv'},  
        },{
            'regex' : r'((pebble))app',                                               # Pebble
            'props' : {'vendor': None, 'model': None, 'type': 'wearable'}, 
        },{
            'regex' : r'droid.+; (glass) \d',                                         # Google Glass
            'props' : {'model': None, 'vendor': 'Google', 'type': 'wearable'},  
        },{
            'regex' : r'droid.+; (wt63?0{2,3})\)',
            'props' : {'model': None, 'vendor': 'Zebra', 'type': 'wearable'},  
        },{
            'regex' : r'(quest( 2)?)',                                                # Oculus Quest
            'props' : {'model': None, 'vendor': 'Facebook', 'type': 'wearable'},  
        },{
            'regex' : r'(tesla)(?: qtcarbrowser|\/[-\w\.]+)',                         # Tesla
            'props' : {'vendor': None, 'type': 'embedded'},  
        },{
            'regex' : r'droid .+?; ([^;]+?)(?: bui|\) applew).+? mobile safari',      # Android Phones from Unidentified Vendors
            'props' : {'model': None, 'type': 'mobile'},  
        },{
            'regex' : r'droid .+?; ([^;]+?)(?: bui|\) applew).+?(?! mobile) safari',  # Android Tablets from Unidentified Vendors
            'props' : {'model': None, 'type': 'tablet'},  
        },{
            'regex' : r'\b((tablet|tab)[;\/]|focus\/\d(?!.+mobile))',                 # Unidentifiable Tablet
            'props' : {'type': 'tablet'},  
        },{
            'regex' : r'(phone|mobile(?:[;\/]| safari)|pda(?=.+windows ce))',         # Unidentifiable Mobile
            'props' : {'type': 'mobile'},  
        },{
            'regex' : r'(android[-\w\. ]{0,9});.+buil',                                # Generic Android Device
            'props' : {'model': None, 'vendor': 'Generic'}
        }
    ],

    'engine': [
        {
            'regex' : r'windows.+ edge\/([\w\.]+)',                           # EdgeHTML
            'props' : {'version': None, 'name': 'EdgeHTML'}, 
        },{
            'regex' : r'webkit\/537\.36.+chrome\/(?!27)([\w\.]+)',            # Blink
            'props' : {'version': None, 'name': 'Blink'}, 
        },{
            'regex' : r'(presto)\/([\w\.]+)',                                         # Presto
            'props' : {'name': None, 'version': None}, 
        },{
            'regex' : r'(webkit|trident|netfront|netsurf|amaya|lynx|w3m|goanna)\/([\w\.]+)',  # WebKit/Trident/NetFront/NetSurf/Amaya/Lynx/w3m/Goanna
            'props' : {'name': None, 'version': None}, 
        },{
            'regex' : r'ekioh(flow)\/([\w\.]+)',                                      # Flow
            'props' : {'name': None, 'version': None}, 
        },{
            'regex' : r'(khtml|tasman|links)[\/ ]\(?([\w\.]+)',                       # KHTML/Tasman/Links
            'props' : {'name': None, 'version': None}, 
        },{
            'regex' : r'(icab)[\/ ]([23]\.[\d\.]+)',                                   # iCab 
            'props' : {'name': None, 'version': None}, 
        },{
            'regex' : r'rv\:([\w\.]{1,9})\b.+(gecko)',                        # Gecko
            'props' : {'version': None, 'name': None}, 
        }
    ],

    'os': [
        {
            'regex' : r'microsoft (windows) (vista|xp)',                            # Windows (iTunes)
            'props' : {'name': None, 'version': None}, 
        },{
            'regex' : r'(windows) nt 6\.2; (arm)',                                    # Windows RT
            'props' : {
                'name'   : None, 
                'version': lambda s: str_mapper(s, WINDOWS_VERSION_MAP)
            }, 
        },{
            'regex' : r'(windows (?:phone(?: os)?|mobile))[\/ ]?([\d\.\w ]*)',        # Windows Phone
            'props' : {
                'name'   : None, 
                'version': lambda s: str_mapper(s, WINDOWS_VERSION_MAP)
            }, 
        },{
            'regex' : r'(windows)[\/ ]?([ntce\d\. ]+\w)(?!.+xbox)',
            'props' : {
                'name'   : None, 
                'version': lambda s: str_mapper(s, WINDOWS_VERSION_MAP)
            }, 
        },{
            'regex' : r'(win(?=3|9|n)|win 9x )([nt\d\.]+)', 
            'props' : {
                'name'   : 'Windows', 
                'version': lambda s: str_mapper(s, WINDOWS_VERSION_MAP)
            }, 
        },{
            'regex' : r'ip[honead]{2,4}\b(?:.*os ([\w]+) like mac|; opera)',          # iOS
            'props' : {
                'version': lambda s: re.sub('_', '.', s), 
                'name'   : 'iOS'
            }, 
        },{
            'regex' : r'cfnetwork\/.+darwin',
            'props' : {
                'version': lambda s: re.sub('_', '.', s), 
                'name'   : 'iOS'
            },
        },{
            'regex' : r'(mac os x) ?([\w\. ]*)',                                    # Mac OS
            'props' : {
                'name'   : 'Mac OS',
                'version': lambda s: re.sub('_', '.', s)
            },
        },{ 
            'regex' : r'(macintosh|mac_powerpc\b)(?!.+haiku)',                      # Mac OS
            'props' : {
                'name'   : 'Mac OS',
                'version': lambda s: re.sub('_', '.', s)
            },
        },{ 
            'regex' : r'droid ([\w\.]+)\b.+(android[- ]x86)',                 # Android-x86
            'props' : {'version': None, 'name': None}, 
        },{
            'regex' : r'(android|webos|qnx|bada|rim tablet os|maemo|meego|sailfish)[-\/ ]?([\w\.]*)',  # Android/WebOS/QNX/Bada/RIM/Maemo/MeeGo/Sailfish OS
            'props' : {'name': None, 'version': None}, 
        },{
            'regex' : r'(blackberry)\w*\/([\w\.]*)',                                  # Blackberry
            'props' : {'name': None, 'version': None}, 
        },{
            'regex' : r'(tizen|kaios)[\/ ]([\w\.]+)',                                 # Tizen/KaiOS
            'props' : {'name': None, 'version': None}, 
        },{
            'regex' : r'\((series40);',                                                # Series 40
            'props' : {'name': None, 'version': None},  
        },{
            'regex' : r'\(bb(10);',                                           # BlackBerry 10
            'props' : {'version': None, 'name': 'BlackBerry'}, 
        },{
            'regex' : r'(?:symbian ?os|symbos|s60(?=;)|series60)[-\/ ]?([\w\.]*)',  # Symbian
            'props' : {'version': None, 'name': 'Symbian'}, 
        },{
            'regex' : r'mozilla\/[\d\.]+ \((?:mobile|tablet|tv|mobile; [\w ]+); rv:.+ gecko\/([\w\.]+)',  # Firefox OS
            'props' : {'version': None, 'name': 'Firefox OS'}, 
        },{
            'regex' : r'web0s;.+rt(tv)',                                   # WebOS
            'props' : {'version': None, 'name': 'webOS'}, 
        },{
            'regex' : r'\b(?:hp)?wos(?:browser)?\/([\w\.]+)',                          # WebOS
            'props' : {'version': None, 'name': 'webOS'}, 
        },{
            'regex' : r'crkey\/([\d\.]+)',                                    # Google Chromecast
            'props' : {'version': None, 'name': 'Chromecast'}, 
        },{
            'regex' : r'(cros) [\w]+ ([\w\.]+\w)',                            # Chromium OS
            'props' : {'name': 'Chromium OS', 'version': None}, 
        },{
            'regex' : r'(nintendo|playstation) ([wids345portablevuch]+)',             # Nintendo/Playstation
            'props' : {'name': None, 'version': None},
        },{ 
            'regex' : r'(xbox); +xbox ([^\);]+)',                                     # Microsoft Xbox (360, One, X, S, Series X, Series S)
            'props' : {'name': None, 'version': None},
        },{ 
            'regex' : '\b(joli|palm)\b ?(?:os)?\/?([\w\.]*)',                        # Joli/Palm
            'props' : {'name': None, 'version': None},
        },{ 
            'regex' : r'(mint)[\/\(\) ]?(\w*)',                                       # Mint
            'props' : {'name': None, 'version': None},
        },{ 
            'regex' : r'(mageia|vectorlinux)[; ]',                                    # Mageia/VectorLinux
            'props' : {'name': None, 'version': None},
        },{ 
            'regex' : r'([kxln]?ubuntu|debian|suse|opensuse|gentoo|arch(?= linux)|slackware|fedora|mandriva|centos|pclinuxos|red ?hat|zenwalk|linpus|raspbian|plan 9|minix|risc os|contiki|deepin|manjaro|elementary os|sabayon|linspire)(?: gnu\/linux)?(?: enterprise)?(?:[- ]linux)?(?:-gnu)?[-\/ ]?(?!chrom|package)([-\w\.]*)',  # Ubuntu/Debian/SUSE/Gentoo/Arch/Slackware/Fedora/Mandriva/CentOS/PCLinuxOS/RedHat/Zenwalk/Linpus/Raspbian/Plan9/Minix/RISCOS/Contiki/Deepin/Manjaro/elementary/Sabayon/Linspire
            'props' : {'name': None, 'version': None},
        },{
            'regex' : r'(hurd|linux) ?([\w\.]*)',                                     # Hurd/Linux
            'props' : {'name': None, 'version': None},
        },{ 
            'regex' : r'(gnu) ?([\w\.]*)',                                            # GNU
            'props' : {'name': None, 'version': None},
        },{ 
            'regex' : r'\b([-frentopcghs]{0,5}bsd|dragonfly)[\/ ]?(?!amd|[ix346]{1,2}86)([\w\.]*)',  # FreeBSD/NetBSD/OpenBSD/PC-BSD/GhostBSD/DragonFly
            'props' : {'name': None, 'version': None},
        },{
            'regex' : r'(haiku) (\w+)',                                                # Haiku
            'props' : {'name': None, 'version': None},
        },{
            'regex' : r'(sunos) ?([\w\.\d]*)',                                # Solaris
            'props' : {'name': 'Solaris', 'version': None}, 
        },{
            'regex' : r'((?:open)?solaris)[-\/ ]?([\w\.]*)',                          # Solaris
            'props' : {'name': None, 'version': None},
        },{
            'regex' : r'(aix) ((\d)(?=\.|\)| )[\w\.])*',                              # AIX
            'props' : {'name': None, 'version': None},
        },{
            'regex' : r'\b(beos|os\/2|amigaos|morphos|openvms|fuchsia|hp-ux)',        # BeOS/OS2/AmigaOS/MorphOS/OpenVMS/Fuchsia/HP-UX
            'props' : {'name': None, 'version': None},
        },{
            'regex' : r'(unix) ?([\w\.]*)',                                            # UNIX
            'props' : {'name': None, 'version': None},
        }
    ]
}

# Compile all regexes
for list_ in wtf.values():
    for dict_ in list_:
        dict_['regex'] = re.compile(dict_['regex'], re.IGNORECASE)



def Mapper(match: re.Match, value: Union[str, Callable] = None) -> str:
    """ Mapper function. Processes a substring returned as the result of re.group function.
        The returned function modifies <m> (= a regex match object) according to the type of the 
        specified <value>. In particular: 
            * If value is None, it returns the corresponding match,
            * if the value is a string, the match is ignored, and the value itself is returned,
            * if the value is a callable (function) it is being applied to the match, and the
              result of that operation is returned.
    """

    if value is None:                   return match if match else None
    elif isinstance(value, str):        return value
    elif isinstance(value, Callable):   return value(match) if match else None


def RegexMapper(ua, arrays):

    if not ua: return None

    # loop through all regexes
    for dict_ in arrays:
        matches = dict_['regex'].search(ua) # try matching uastring with regexes
        if matches: break
    
    if matches:

        for i, (key, value) in enumerate(dict_['props'].items()):

            try              : match = matches.group(i + 1)
            except IndexError: match = None
            
            yield key, Mapper(match, value)

if __name__ == '__main__':

    uaStrings = [
    'Mozilla/5.0 (Linux; Android 10; Quest 2) AppleWebKit/537.36 (KHTML, like Gecko) OculusBrowser/23.0.0.1.18.389879693 SamsungBrowser/4.0 Chrome/104.0.5112.69 Mobile VR Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; Quest 2) AppleWebKit/537.36 (KHTML, like Gecko) OculusBrowser/22.3.0.5.34.384414863 SamsungBrowser/4.0 Chrome/102.0.5005.148 Mobile VR Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; Quest 2) AppleWebKit/537.36 (KHTML, like Gecko) OculusBrowser/22.2.0.3.39.382455783 SamsungBrowser/4.0 Chrome/102.0.5005.148 Mobile VR Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; Quest 2) AppleWebKit/537.36 (KHTML, like Gecko) OculusBrowser/22.1.0.2.42.378269191 SamsungBrowser/4.0 Chrome/102.0.5005.99 Mobile VR Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; Quest 2) AppleWebKit/537.36 (KHTML, like Gecko) OculusBrowser/21.2.0.1.37.371181431 SamsungBrowser/4.0 Chrome/100.0.4896.160 Mobile VR Safari/537.36',
    'Mozilla/5.0 (Linux; Android 7.1.1; Pacific Build/N9F27L) AppleWebKit/537.36 (KHTML, like Gecko) OculusBrowser/4.0.0.17 SamsungBrowser/4.0 Chrome/61.0.3163.109 Mobile VR Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; Quest 2) AppleWebKit/537.36 (KHTML, like Gecko) OculusBrowser/19.1.0.1.50.350517500 SamsungBrowser/4.0 Chrome/96.0.4664.174 Mobile VR Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; Quest) AppleWebKit/537.36 (KHTML, like Gecko) OculusBrowser/19.1.0.1.50.350517500 SamsungBrowser/4.0 Chrome/96.0.4664.174 Mobile VR Safari/537.36',
    'Mozilla/5.0 (Linux; Android 7.0; SM-G920W8) AppleWebKit/537.36 (KHTML, like Gecko) OculusBrowser/8.1.5.203450095 SamsungBrowser/4.0 Chrome/79.0.3945.126 Mobile VR Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; Quest 2) AppleWebKit/537.36 (KHTML, like Gecko) OculusBrowser/18.4.0.2.24.345749361 SamsungBrowser/4.0 Chrome/95.0.4638.74 Mobile VR Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; Quest 2) AppleWebKit/537.36 (KHTML, like Gecko) OculusBrowser/18.1.0.2.46.337441587 SamsungBrowser/4.0 Chrome/95.0.4638.74 Mobile VR Safari/537.36',
    'Mozilla/5.0 (Linux; Android 7.1.1; Quest) AppleWebKit/537.36 (KHTML, like Gecko) OculusBrowser/13.4.0.6.15.271681329 SamsungBrowser/4.0 Chrome/87.0.4280.141 Mobile VR Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; Quest 2) AppleWebKit/537.36 (KHTML, like Gecko) OculusBrowser/17.2.0.9.61.329948727 SamsungBrowser/4.0 Chrome/93.0.4577.82 Mobile VR Safari/537.36',
    'Mozilla/5.0 (Linux; Android 7.1.1; Pacific) AppleWebKit/537.36 (KHTML, like Gecko) OculusBrowser/10.16.0.0.0.296461555 SamsungBrowser/4.0 Chrome/91.0.4472.88 Mobile VR Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; Quest 2) AppleWebKit/537.36 (KHTML, like Gecko) OculusBrowser/17.0.0.6.22.318015459 SamsungBrowser/4.0 Chrome/93.0.4577.62 VR Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; Quest 2) AppleWebKit/537.36 (KHTML, like Gecko) OculusBrowser/16.6.0.1.52.314146309 SamsungBrowser/4.0 Chrome/91.0.4472.164 VR Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; Quest) AppleWebKit/537.36 (KHTML, like Gecko) OculusBrowser/16.6.0.1.52.314146309 SamsungBrowser/4.0 Chrome/91.0.4472.164 VR Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; Quest 2) AppleWebKit/537.36 (KHTML, like Gecko) OculusBrowser/16.5.0.1.41.311050207 SamsungBrowser/4.0 Chrome/91.0.4472.164 VR Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; Quest) AppleWebKit/537.36 (KHTML, like Gecko) OculusBrowser/16.4.0.1.51.307961319 SamsungBrowser/4.0 Chrome/91.0.4472.164 VR Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; Quest) AppleWebKit/537.36 (KHTML, like Gecko) OculusBrowser/16.3.0.2.35.305078360 SamsungBrowser/4.0 Chrome/91.0.4472.164 VR Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; Quest 2) AppleWebKit/537.36 (KHTML, like Gecko) OculusBrowser/16.3.0.2.35.305078360 SamsungBrowser/4.0 Chrome/91.0.4472.164 VR Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; Quest 2) AppleWebKit/537.36 (KHTML, like Gecko) OculusBrowser/16.2.0.4.37.303893781 SamsungBrowser/4.0 Chrome/91.0.4472.114 VR Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; SM-G965F) AppleWebKit/537.36 (KHTML, like Gecko) OculusBrowser/8.1.5.203450095 SamsungBrowser/4.0 Chrome/79.0.3945.126 Mobile VR Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; Quest) AppleWebKit/537.36 (KHTML, like Gecko) OculusBrowser/16.1.0.3.48.300946211 SamsungBrowser/4.0 Chrome/91.0.4472.114 VR Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; Quest) AppleWebKit/537.36 (KHTML, like Gecko) OculusBrowser/16.0.0.4.13.298796165 SamsungBrowser/4.0 Chrome/91.0.4472.88 VR Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; Quest 2) AppleWebKit/537.36 (KHTML, like Gecko) OculusBrowser/6.0.13.162924334 SamsungBrowser/4.0 Chrome/74.0.3729.182 VR Safari/537.36',
    'Mozilla/5.0 (Linux; Android 7.0; SM-G920F) AppleWebKit/537.36 (KHTML, like Gecko) OculusBrowser/8.1.5.203450095 SamsungBrowser/4.0 Chrome/79.0.3945.126 Mobile VR Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/119.0.1084.56 Safari/536.5 Comodo_Dragon/109.2.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Comodo_Dragon/104.0',
    'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.7 (KHTML, like Gecko) Comodo_Dragon/91.0.4472.164 Chrome/75.0.3770.100 Safari/535.7',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.11 (KHTML, like Gecko) Comodo_Dragon/37.1.0.0 Chrome/37.0.963.38 Safari/535.11',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Comodo_Dragon/37.1.0.0 Chrome/37.0.963.38 Safari/535.11',
    'Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.83 Safari/537.1 Comodo_Dragon/21.1.1.0',
    'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.75 Safari/537.1 Comodo_Dragon/21.0.2.0',
    'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.83 Safari/537.1 Comodo_Dragon/21.1.1.0',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.75 Safari/537.1 Comodo_Dragon/21.0.2.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.83 Safari/537.1 Comodo_Dragon/21.1.1.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.75 Safari/537.1 Comodo_Dragon/21.0.2.0',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.83 Safari/537.1 Comodo_Dragon/21.1.1.0',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.75 Safari/537.1 Comodo_Dragon/21.0.2.0',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.83 Safari/537.1 Comodo_Dragon/21.1.1.0',
    'Mozilla/5.0 (Windows NT 5.0) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.75 Safari/537.1 Comodo_Dragon/21.0.2.0',
    'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.41 Safari/537.1 Comodo_Dragon/21.0.0.0',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.75 Safari/537.1 Comodo_Dragon/21.0.2.0',
    'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11 Comodo_Dragon/20.1.1.0',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.47 Safari/536.11 Comodo_Dragon/20.0.1.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.47 Safari/536.11 Comodo_Dragon/20.0.1.0',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.47 Safari/536.11 Comodo_Dragon/20.0.1.0',
    'Mozilla/5.0 (Windows NT 5.2) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11 Comodo_Dragon/20.1.1.0',
    'Mozilla/5.0 (Windows NT 5.2; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.47 Safari/536.11 Comodo_Dragon/20.0.1.0',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11 Comodo_Dragon/20.1.1.0',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11 Comodo_Dragon/20.1.1.0',
    'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.47 Safari/536.11 Comodo_Dragon/20.0.1.0',
    'Mozilla/5.0 (Windows NT 5.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11 Comodo_Dragon/20.1.1.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11 Comodo_Dragon/20.1.1.0',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.47 Safari/536.11 Comodo_Dragon/20.0.1.0',
    'Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.47 Safari/536.11 Comodo_Dragon/20.0.1.0',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11 Comodo_Dragon/20.1.1.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11 Comodo_Dragon/20.1.1.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46 Safari/536.5 Comodo_Dragon/19.0.3.0',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5 Comodo_Dragon/19.1.0.0',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.56 Safari/536.5 Comodo_Dragon/19.2.0.0',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.56 Safari/536.5 Comodo_Dragon/19.2.0.0',
    'Mozilla/5.0 (Windows NT 5.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46 Safari/536.5 Comodo_Dragon/19.0.3.0',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46 Safari/536.5 Comodo_Dragon/19.0.3.0',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.56 Safari/536.5 Comodo_Dragon/19.2.0.0',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46 Safari/536.5 Comodo_Dragon/19.0.3.0',
    'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.56 Safari/536.5 Comodo_Dragon/19.2.0.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.56 Safari/536.5 Comodo_Dragon/19.2.0.0',
    'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46 Safari/536.5 Comodo_Dragon/19.0.3.0',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46 Safari/536.5 Comodo_Dragon/19.0.3.0',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5 Comodo_Dragon/19.1.0.0',
    'Mozilla/5.0 (Windows NT 5.2) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.56 Safari/536.5 Comodo_Dragon/19.2.0.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5 Comodo_Dragon/19.1.0.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.140 Safari/535.19 Comodo_Dragon/18.0.3.0',
    'Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.152 Safari/535.19 Comodo_Dragon/18.1.2.0',
    'Mozilla/5.0 (Windows NT 5.1; WOW64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.152 Safari/535.19 Comodo_Dragon/18.1.2.0',
    'Mozilla/5.0 (Macintosh; PowerPC Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
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
    ii  = 0
    for ua in uaStrings:
        ii += 1

        _browser, _cpu, _device, _engine, _os = test(ua)

        for key, value in RegexMapper(ua,  wtf['browser']): 
            out.append(value == _browser[key])
            if not value == _browser[key]:
                print('browser:', key, '->', ua)

        for key, value in RegexMapper(ua,  wtf['cpu']): 
            out.append(value == _cpu[key])
            if not value == _cpu[key]:
                print('cpu:', key, '->', ua)
        
        for key, value in RegexMapper(ua,  wtf['device']): 
            out.append(value == _device[key])
            if not value == _device[key]:
                print('device:', key, '->', ua)
        
        for key, value in RegexMapper(ua,  wtf['engine']): 
            out.append(value == _engine[key])
            if not value == _engine[key]:
                print('engine:', key, '->', ua)
        
        for key, value in RegexMapper(ua,  wtf['os']): 
            out.append(value == _os[key])
            if not value == _os[key]:
                print('os:', key, '->', ua)
            

    c = all(out)
    print(f'Tested {ii} user agents. All correct: {c}')