import re
from .utils import strMapper


EMPTY = '' # Empty pattern

# Old safari version mapper
SAFARI_VERSIONS = {
    '/8'   : '1.0',
    '/1'   : '1.2',
    '/3'   : '1.3',
    '/412' : '2.0',
    '/416' : '2.0.2',
    '/417' : '2.0.3',
    '/419' : '2.0.4',
    '/'    : '?' # Unknown version
}

# Windows version kapper
WINDOWS_VERSIONS = {
    '4.90'   : 'ME',
    'NT3.51' :'NT 3.11',
    'NT4.0'  :'NT 4.0',
    'NT 5.0' :'2000',
    'NT 5.1' :'XP',
    'NT 5.2' :'XP',
    'NT 6.0' :'Vista',
    'NT 6.1' :'7',
    'NT 6.2' :'8',
    'NT 6.3' :'8.1',
    'NT 6.4' :'10',
    'NT 10.0':'10',
    'ARM'    :'RT',
}

""" Regex lists """
BROWSER = [
    {   # Chrome for Android/iOS
        'regex' : r'\b(?:crmo|crios)\/([\w\.]+)',                           
        'props' : {'version': None, 'name': 'Chrome'}
    },{ # Microsoft Edge
        'regex' : r'edg(?:e|ios|a)?\/([\w\.]+)',                          
        'props' : {'version': None, 'name': 'Edge'}
    },{ # Opera Mini
        'regex' : r'(opera mini)\/([-\w\.]+)',                              
        'props' : {'name': None, 'version': None}
    },{ # Opera Mobi/Tablet
        'regex' : r'(opera [mobiletab]{3,6})\b.+version\/([-\w\.]+)',       
        'props' : {'name': None, 'version': None}
    },{ # Opera
        'regex' : r'(opera)(?:.+version\/|[\/ ]+)([\w\.]+)',                
        'props' : {'name': None, 'version': None}
    },{ # Opera mini on iphone >= 8.0
        'regex' : r'opios[\/ ]+([\w\.]+)',                                  
        'props' : {'version': None, 'name': 'Opera Mini'}
    },{ # Opera Webkit
        'regex' : r'\bopr\/([\w\.]+)',                                      
        'props' : {'version': None, 'name': 'Opera'}
    },{ # Kindle
        'regex' : r'(kindle)\/([\w\.]+)',                                 
        'props' : {'name': None, 'version': None}
    },{ # Lunascape/Maxthon/Netfront/Jasmine/Blazer
        'regex' : r'(lunascape|maxthon|netfront|jasmine|blazer)[\/ ]?([\w\.]*)',  
        'props' : {'name': None, 'version': None}
    },{ # Avant/IEMobile/SlimBrowser
        'regex' : r'(avant |iemobile|slim)(?:browser)?[\/ ]?([\w\.]*)',           
        'props' : {'name': None, 'version': None}
    },{ # Baidu Browser
        'regex' : r'(ba?idubrowser)[\/ ]?([\w\.]+)',
        'props' : {'name': None, 'version': None}
    },{ # Internet Explorer
        'regex' : r'(?:ms|\()(ie) ([\w\.]+)',
        'props' : {'name': None, 'version': None}
    },{ # Rekonq/Puffin/Brave/Whale/QQBrowserLite/QQ, aka ShouQ
        'regex' : r'(flock|rockmelt|midori|epiphany|silk|skyfire|ovibrowser|bolt|iron|vivaldi|iridium|phantomjs|bowser|quark|qupzilla|falkon|rekonq|puffin|brave|whale|qqbrowserlite|qq)\/([-\w\.]+)',  
        'props' : {'name': None, 'version': None}
    },{ # Weibo
        'regex' : r'(weibo)__([\d\.]+)',
        'props' : {'name': None, 'version': None}
    },{ # UCBrowser
        'regex' : r'(?:\buc? ?browser|(?:juc.+)ucweb)[\/ ]?([\w\.]+)',
        'props' : {'version': None, 'name': 'UCBrowser'}, 
    },{ # WeChat Desktop for Windows Built-in Browser
        'regex' : r'\bqbcore\/([\w\.]+)',
        'props' : {'version': None, 'name': 'WeChat(Win) Desktop'}, 
    },{ # WeChat
        'regex' : r'micromessenger\/([\w\.]+)',
        'props' : {'version': None, 'name': 'WeChat'}, 
    },{ # Konqueror
        'regex' : r'konqueror\/([\w\.]+)',
        'props' : {'version': None, 'name': 'Konqueror'}, 
    },{ # IE11
        'regex' : r'trident.+rv[: ]([\w\.]{1,9})\b.+like gecko',
        'props' : {'version': None, 'name': 'IE'} 
    },{ # Yandex
        'regex' : r'yabrowser\/([\w\.]+)',
        'props' : {'version': None, 'name': 'Yandex'}, 
    },{ # Avast/AVG Secure Browser
        'regex' : r'(avast|avg)\/([\w\.]+)',
        'props' : {
            'name'   : lambda s: re.sub(r'(.+)', '\\1 Secure Browser', s),
            'version': None
            }
    },{ # Firefox Focus
        'regex' : r'\bfocus\/([\w\.]+)',                                  
        'props' : {'version': None, 'name': 'Firefox Focus'}, 
    },{ # Opera Touch
        'regex' : r'\bopt\/([\w\.]+)',                                    
        'props' : {'version': None, 'name': 'Opera Touch'}, 
    },{ # Coc Coc Browser 
        'regex' :  r'coc_coc\w+\/([\w\.]+)',                              
        'props' : {'version': None, 'name': 'Coc Coc'},
    },{ # Dolphin
        'regex' : r'dolfin\/([\w\.]+)',                                   
        'props' : {'version': None, 'name': 'Dolphin'}, 
    },{ # Opera Coast
        'regex' : r'coast\/([\w\.]+)',                                    
        'props' : {'version': None, 'name': 'Opera Coast'}, 
    },{ # MIUI Browser
        'regex' : r'miuibrowser\/([\w\.]+)',                              
        'props' : {'version': None, 'name': 'MIUI Browser'}, 
    },{ # Firefox for iOS
        'regex' : r'fxios\/([-\w\.]+)',                                   
        'props' : {'version': None, 'name': 'Firefox'}, 
    },{ # 360
        'regex' : r'\bqihu|(qi?ho?o?|360)browser',                        
        'props' : {'name': '360 Browser'},  
    },{ # Oculus/Samsung/Sailfish Browser 
        'regex' : r'(oculus|samsung|sailfish)browser\/([\w\.]+)',
        'props' : {
            'name'   : lambda s: re.sub(r'(.+)', '\\1 Browser', s),
            'version': None
            },
    },{ # Comodo Dragon
        'regex' : r'(comodo_dragon)\/([\w\.]+)',
        'props' : {
            'name'   : lambda s: re.sub(r'_', ' ', s), 
            'version': None
            }, 
    },{ # Electron-based App
        'regex' : r'(electron)\/([\w\.]+) safari',
        'props' : {'name': None, 'version': None}
    },{ # Tesla
        'regex' : r'(tesla)(?: qtcarbrowser|\/(20\d\d\.[-\w\.]+))',
        'props' : {'name': None, 'version': None}
    },{ # QQBrowser/Baidu App/2345 Browser
        'regex' : r'm?(qqbrowser|baiduboxapp|2345Explorer)[\/ ]?([\w\.]+)',
        'props' : {'name': None, 'version': None}
    },{ # SouGouBrowser
        'regex' : r'(metasr)[\/ ]?([\w\.]+)',
        'props' : {'name': None} 
    },{ # LieBao Browser
        'regex' : r'(lbbrowser)',
        'props' : {'name': None}, 
    },{ # Facebook App for iOS & Android
        'regex' : r'((?:fban\/fbios|fb_iab\/fb4a)(?!.+fbav)|;fbav\/([\w\.]+);)', 
        'props' : {'name': 'Facebook', 'version': None},                        
    },{ # Line App for iOS
        'regex' : r'safari (line)\/([\w\.]+)',
        'props' : {'name': None, 'version': None}, 
    },{ # Line App for Android
        'regex' : r'\b(line)\/([\w\.]+)\/iab',
        'props' : {'name': None, 'version': None}, 
    },{ # Chromium/Instagram
        'regex' : r'(chromium|instagram)[\/ ]([-\w\.]+)',
        'props' : {'name': None, 'version': None}, 
    },{ # Google Search Appliance on iOS
        'regex' : r'\bgsa\/([\w\.]+) .*safari\/',
        'props' : {'version': None, 'name': 'GSA'},                             
    },{ # Chrome Headless
        'regex' : r'headlesschrome(?:\/([\w\.]+)| )',
        'props' : {'version': None, 'name': 'Chrome Headless'},            
    },{ # Chrome WebView
        'regex' : r' wv\).+(chrome)\/([\w\.]+)',
        'props' : {'name': 'Chrome WebView', 'version': None},             
    },{ # Android Browser
        'regex' : r'droid.+ version\/([\w\.]+)\b.+(?:mobile safari|safari)',
        'props' : {'version': None, 'name': 'Android Browser'},            
    },{ # Chrome/OmniWeb/Arora/Tizen/Nokia
        'regex' : r'(chrome|omniweb|arora|[tizenoka]{5} ?browser)\/v?([\w\.]+)',
        'props' : {'name': None, 'version': None},                                      
    },{ # Mobile Safari
        'regex' : r'version\/([\w\.]+) .*mobile\/\w+ (safari)',
        'props' : {'version': None, 'name': 'Mobile Safari'},                   
    },{ # Safari & Safari Mobile
        'regex' : r'version\/([\w\.]+) .*(mobile ?safari|safari)',
        'props' : {'version': None, 'name': None},                                      
    },{ # Safari < 3.0 
        'regex' : r'webkit.+?(mobile ?safari|safari)(\/[\w\.]+)',
        'props' : {
            'name'   : None,                                                           
            'version': lambda s: strMapper(s, SAFARI_VERSIONS)
            },        
    },{
        'regex' : r'(webkit|khtml)\/([\w\.]+)', 
        'props' : {'name': None, 'version': None}, 
    },{ # Netscape 
        'regex' : r'(navigator|netscape\d?)\/([-\w\.]+)',                           
        'props' : {'name': 'Netscape', 'version': None},
    },{ # Firefox Reality
        'regex' : r'mobile vr; rv:([\w\.]+)\).+firefox',                            
        'props' : {'version': None, 'name': 'Firefox Reality'},            
    },{ # Flow
        'regex' : r'ekiohf.+(flow)\/([\w\.]+)',                                   
        'props' : {'name': None, 'version': None}
    },{ # Swiftfox
        'regex' : r'(swiftfox)',
        'props' : {'name': None, 'version': None}
    },{ # IceDragon/Iceweasel/Camino/Chimera/Fennec/Maemo/Minimo/Conkeror/Klar
        'regex' : r'(icedragon|iceweasel|camino|chimera|fennec|maemo browser|minimo|conkeror|klar)[\/ ]?([\w\.\+]+)',                         
        'props' : {'name': None, 'version': None}
    },{ # Firefox/SeaMonkey/K-Meleon/IceCat/IceApe/Firebird/Phoenix
        'regex' : r'(seamonkey|k-meleon|icecat|iceape|firebird|phoenix|palemoon|basilisk|waterfox)\/([-\w\.]+)$',                             
        'props' : {'name': None, 'version': None}
    },{ # Other Firefox-based
        'regex' : r'(firefox)\/([\w\.]+)',                                        
        'props' : {'name': None, 'version': None}
    },{ # Mozilla
        'regex' : r'(mozilla)\/([\w\.]+) .+rv\:.+gecko\/\d+',                     
        'props' : {'name': None, 'version': None}
    },{ # Polaris/Lynx/Dillo/iCab/Doris/Amaya/w3m/NetSurf/Sleipnir/Obigo/Mosaic/Go/ICE/UP.Browser
        'regex' : r'(polaris|lynx|dillo|icab|doris|amaya|w3m|netsurf|sleipnir|obigo|mosaic|(?:go|ice|up)[\. ]?browser)[-\/ ]?v?([\w\.]+)',
        'props' : {'name': None, 'version': None}
    },{ # Links
        'regex' : r'(links) \(([\w\.]+)',
        'props' : {'name': None, 'version': None}
    }
]

CPU =  [
    {   # AMD64 (x64)
        'regex' : r'(?:(amd|x(?:(?:86|64)[-_])?|wow|win)64)[;\)]',
        'props' : {'architecture': 'amd64'},                              
    },{ # IA32 (quicktime)
        'regex' : r'(ia32(?=;))',                                         
        'props' : {'architecture': lambda s: s.lower()},                       
    },{ # IA32 (x86)
        'regex' : r'((?:i[346]|x)86)[;\)]',                               
        'props' : {'architecture': 'ia32'}, 
    },{ # ARM64
        'regex' : r'\b(aarch64|arm(v?8e?l?|_?64))\b',                     
        'props' : {'architecture': 'arm64'}, 
    },{ # ARMHF
        'regex' : r'\b(arm(?:v[67])?ht?n?[fl]p?)\b',                      
        'props' : {'architecture': 'armhf'}, 
    },{ # PocketPC mistakenly identified as PowerPC
        'regex' : r'windows (ce|mobile); ppc;',                           
        'props' : {'architecture': 'arm'},  
    },{ # PowerPC
        'regex' : r'((?:ppc|powerpc)(?:64)?)(?: mac|;|\))',               
        'props' : {'architecture': lambda s: re.sub(r'ower', EMPTY, s).lower()},
    },{ # SPARC
        'regex' : r'(sun4\w)[;\)]',                                       
        'props' : {'architecture': 'sparc'}, 
    },{ # IA64, 68K, ARM/64, AVR/32, IRIX/64, MIPS/64, SPARC/64, PA-RISC
        'regex' : r'((?:avr32|ia64(?=;))|68k(?=\))|\barm(?=v(?:[1-7]|[5-7]1)l?|;|eabi)|(?=atmel )avr|(?:irix|mips|sparc)(?:64)?\b|pa-risc)',  
        'props' : {'architecture': lambda s: s.lower()}                              
    }
]

DEVICE =  [
    {   # Samsung devices 
        'regex' : r'\b(sch-i[89]0\d|shw-m380s|sm-[pt]\w{2,4}|gt-[pn]\d{2,4}|sgh-t8[56]9|nexus 10)',   
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
    },{ # iPod/iPhone
        'regex' : r'\((ip(?:hone|od)[\w ]*);',
        'props' : {'model': None, 'vendor': 'Apple', 'type': 'mobile'}, 
    },{ # iPad
        'regex' : r'\((ipad);[-\w\),; ]+apple',
        'props' : {'model': None, 'vendor': 'Apple', 'type': 'tablet'}, 
    },{
        'regex' : r'applecoremedia\/[\w\.]+ \((ipad)', 
        'props' : {'model': None, 'vendor': 'Apple', 'type': 'tablet'}, 
    },{
        'regex' : r'\b(ipad)\d\d?,\d\d?[;\]].+ios', 
        'props' : {'model': None, 'vendor': 'Apple', 'type': 'tablet'}, 
    },{ # Huawei
        'regex' : r'\b((?:ag[rs][23]?|bah2?|sht?|btv)-a?[lw]\d{2})\b(?!.+d\/s)',
        'props' : {'model': None, 'vendor': 'Huawei', 'type': 'tablet'}, 
    },{
        'regex' : r'(?:huawei|honor)([-\w ]+)[;\)]', 
        'props' : {'model': None, 'vendor': 'Huawei', 'type': 'tablet'}, 
    },{
        'regex' : r'\b(nexus 6p|\w{2,4}-[atu]?[ln][01259x][012359][an]?)\b(?!.+d\/s)', 
        'props' : {'model': None, 'vendor': 'Huawei', 'type': 'mobile'}, 
    },{ # Xiaomi POCO
        'regex' : r'\b(poco[\w ]+)(?: bui|\))',
        'props' : {
            'model'  : lambda s: re.sub('_', ' ', s), 
            'vendor' : 'Xiaomi', 
            'type'   : 'mobile'
            }, 
    },{ # Xiaomi Hongmi 'numeric' models
        'regex' : r'\b; (\w+) build\/hm\1', 
        'props' : {
            'model'  : lambda s: re.sub('_', ' ', s), 
            'vendor' : 'Xiaomi', 
            'type'   : 'mobile'
            }, 
    },{ # Xiaomi Hongmi
        'regex' : r'\b(hm[-_ ]?note?[_ ]?(?:\d\w)?) bui',
        'props' : {
            'model'  : lambda s: re.sub('_', ' ', s), 
            'vendor' : 'Xiaomi', 
            'type'   : 'mobile'
            }, 
    },{ # Xiaomi Redmi
        'regex' : r'\b(redmi[\-_ ]?(?:note|k)?[\w_ ]+)(?: bui|\))',
        'props' : {
            'model'  : lambda s: re.sub('_', ' ', s), 
            'vendor' : 'Xiaomi', 
            'type'   : 'mobile'
            }, 
    },{ # Xiaomi Mi
        'regex' : r'\b(mi[-_ ]?(?:a\d|one|one[_ ]plus|note lte|max)?[_ ]?(?:\d?\w?)[_ ]?(?:plus|se|lite)?)(?: bui|\))',
        'props' : {
            'model'  : lambda s: re.sub('_', ' ', s), 
            'vendor' : 'Xiaomi', 
            'type'   : 'mobile'
            }, 
    },{ # Mi Pad tablets
        'regex' : r'\b(mi[-_ ]?(?:pad)(?:[\w_ ]+))(?: bui|\))',
        'props' : {
            'model'  : lambda s: re.sub('_', ' ', s), 
            'vendor' : 'Xiaomi', 
            'type'   : 'tablet'
            }, 
    },{ # OPPO
        'regex' : r'; (\w+) bui.+ oppo',
        'props' : {'model': None, 'vendor': 'OPPO', 'type': 'mobile'}
    },{
        'regex' : r'\b(cph[12]\d{3}|p(?:af|c[al]|d\w|e[ar])[mt]\d0|x9007|a101op)\b', 
        'props' : {'model': None, 'vendor': 'OPPO', 'type': 'mobile'}
    },{ # Vivo
        'regex' : r'vivo (\w+)(?: bui|\))',
        'props' : {'model': None, 'vendor': 'Vivo', 'type': 'mobile'}
    },{ 
        'regex' : r'\b(v[12]\d{3}\w?[at])(?: bui|;)',
        'props' : {'model': None, 'vendor': 'Vivo', 'type': 'mobile'}
    },{ # Realme
        'regex' : r'\b(rmx[12]\d{3})(?: bui|;|\))',
        'props' : {'model': None, 'vendor': 'Realme', 'type': 'mobile'}
    },{ # Motorola
        'regex' : r'\b(milestone|droid(?:[2-4x]| (?:bionic|x2|pro|razr))?:?( 4g)?)\b[\w ]+build\/',
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
    },{ # Lenovo 
        'regex' : r'(ideatab[-\w ]+)',
        'props' : {'model': None, 'vendor': 'Lenovo', 'type': 'tablet'},  
    },{
        'regex' : r'lenovo ?(s[56]000[-\w]+|tab(?:[\w ]+)|yt[-\d\w]{6}|tb[-\d\w]{6})', 
        'props' : {'model': None, 'vendor': 'Lenovo', 'type': 'tablet'},  
    },{ # Nokia
        'regex' : r'(?:maemo|nokia).*(n900|lumia \d+)',
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
    },{ # Google Pixel C
        'regex' : r'(pixel c)\b',
        'props' : {'model': None, 'vendor': 'Google', 'type': 'tablet'},
    },{ # Google Pixel
        'regex' : r'droid.+; (pixel[\daxl ]{0,6})(?: bui|\))',
        'props' : {'model': None, 'vendor': 'Google', 'type': 'mobile'},
    },{ # Sony
        'regex' : r'droid.+ ([c-g]\d{4}|so[-gl]\w+|xq-a\w[4-7][12])(?= bui|\).+chrome\/(?![1-6]{0,1}\d\.))', 
        'props' : {'model': None, 'vendor': 'Sony', 'type': 'mobile'},
    },{
        'regex' : r'sony tablet [ps]', 
        'props' : {'model': 'Xperia Tablet', 'vendor': 'Sony', 'type': 'tablet'}, 
    },{
        'regex' : r'\b(?:sony)?sgp\w+(?: bui|\))', 
        'props' : {'model': 'Xperia Tablet', 'vendor': 'Sony', 'type': 'tablet'}, 
    },{ # OnePlus
        'regex' : r' (kb2005|in20[12]5|be20[12][59])\b',
        'props' : {'model': None, 'vendor': 'OnePlus', 'type': 'mobile'}, 
    },{
        'regex' : r'(?:one)?(?:plus)? (a\d0\d\d)(?: b|\))', 
        'props' : {'model': None, 'vendor': 'OnePlus', 'type': 'mobile'}, 
    },{ # Amazon
        'regex' : r'(alexa)webm',
        'props' : {'model': None, 'vendor': 'Amazon', 'type': 'tablet'}, 
    },{ # Kindle Fire without Silk
        'regex' : r'(kf[a-z]{2}wi)( bui|\))',
        'props' : {'model': None, 'vendor': 'Amazon', 'type': 'tablet'}, 
    },{ # Kindle Fire HD
        'regex' : r'(kf[a-z]+)( bui|\)).+silk\/',
        'props' : {'model': None, 'vendor': 'Amazon', 'type': 'tablet'}, 
    },{ # Fire Phone
        'regex' : r'((?:sd|kf)[0349hijorstuw]+)( bui|\)).+silk\/',
        'props' : {
            'model'  : lambda s: re.sub(r'(.+)', 'Fire Phone \\1', s), 
            'vendor' : 'Amazon', 
            'type'   : 'mobile'
            }, 
    },{ # BlackBerry PlayBook
        'regex' : r'(playbook);[-\w\),; ]+(rim)',
        'props' : {'model': None, 'vendor' : None, 'type': 'tablet'},
    },{ # BlackBerry 10
        'regex' : r'\b((?:bb[a-f]|st[hv])100-\d)',
        'props' : {'model': None, 'vendor': 'BlackBerry', 'type': 'mobile'}, 
    },{ # BlackBerry 10
        'regex' : r'\(bb10; (\w+)',
        'props' : {'model': None, 'vendor': 'BlackBerry', 'type': 'mobile'}, 
    },{ # Asus
        'regex' : r'(?:\b|asus_)(transfo[prime ]{4,10} \w+|eeepc|slider \w+|nexus 7|padfone|p00[cj])',
        'props' : {'model': None, 'vendor': 'ASUS', 'type': 'tablet'}, 
    },{
        'regex' : r' (z[bes]6[027][012][km][ls]|zenfone \d\w?)\b', 
        'props' : {'model': None, 'vendor': 'ASUS', 'type': 'mobile'}, 
    },{ # HTC Nexus 9
        'regex' : r'(nexus 9)',
        'props' : {'model': None, 'vendor': 'HTC', 'type': 'tablet'}, 
    },{ # HTC
        'regex' : r'(htc)[-;_ ]{1,2}([\w ]+(?=\)| bui)|\w+)',
        'props' : {
            'vendor': None, 
            'model' : lambda s: re.sub('_', ' ', s), 
            'type'  : 'mobile'
            },
    },{ # ZTE
        'regex' : r'(zte)[- ]([\w ]+?)(?: bui|\/|\))',
        'props' : {
            'vendor': None, 
            'model' : lambda s: re.sub('_', ' ', s),
            'type'  : 'mobile'}
    },{ # Alcatel/GeeksPhone/Nexian/Panasonic/Sony
        'regex' : r'(alcatel|geeksphone|nexian|panasonic|sony)[-_ ]?([-\w]*)',
        'props' : {
            'vendor': None, 
            'model' : lambda s: re.sub('_', ' ', s),
            'type'  : 'mobile'}
    },{ # Acer
        'regex' : r'droid.+; ([ab][1-7]-?[0178a]\d\d?)',
        'props' : {'model': None, 'vendor': 'Acer', 'type': 'tablet'}, 
    },{ # Meizu
        'regex' : r'\bmz-([-\w]{2,})',
        'props' : {'model': None, 'vendor': 'Meizu', 'type': 'mobile'}, 
    },{ # Meizu
        'regex' : r'droid.+; (m[1-5] note) bui',
        'props' : {'model': None, 'vendor': 'Meizu', 'type': 'mobile'}, 
    },{ # Sharp
        'regex' : r'\b(sh-?[altvz]?\d\d[a-ekm]?)',
        'props' : {'model': None, 'vendor': 'Sharp', 'type': 'mobile'}, 
    },{ # BlackBerry/BenQ/Palm/Sony-Ericsson/Acer/Asus/Dell/Meizu/Motorola/Polytron
        'regex' : r'(blackberry|benq|palm(?=\-)|sonyericsson|acer|asus|dell|meizu|motorola|polytron)[-_ ]?([-\w]*)',
        'props' : {'vendor': None, 'model': None, 'type': 'mobile'}, 
    },{ # HP iPAQ
        'regex' : r'(hp) ([\w ]+\w)',
        'props' : {'vendor': None, 'model': None, 'type': 'mobile'},  
    },{  # Asus
        'regex' : r'(asus)-?(\w+)',
        'props' : {'vendor': None, 'model': None, 'type': 'mobile'}, 
    },{ # Microsoft Lumia
        'regex' : r'(microsoft); (lumia[\w ]+)',
        'props' : {'vendor': None, 'model': None, 'type': 'mobile'}, 
    },{ # Lenovo
        'regex' : r'(lenovo)[-_ ]?([-\w]+)',
        'props' : {'vendor': None, 'model': None, 'type': 'mobile'}, 
    },{ # Jolla
        'regex' : r'(jolla)',
        'props' : {'vendor': None, 'model': None, 'type': 'mobile'}, 
    },{ # OPPO
        'regex' : r'(oppo) ?([\w ]+) bui',
        'props' : {'vendor': None, 'model': None, 'type': 'mobile'}, 
    },{ # Archos
        'regex' : r'(archos) (gamepad2?)',                                                
        'props' : {'vendor': None, 'model': None, 'type': 'tablet'}, 
    },{ # HP TouchPad
        'regex' : r'(hp).+(touchpad(?!.+tablet)|tablet)',                                 
        'props' : {'vendor': None, 'model': None, 'type': 'tablet'}, 
    },{ # Kindle
        'regex' : r'(kindle)\/([\w\.]+)',                                                 
        'props' : {'vendor': None, 'model': None, 'type': 'tablet'}, 
    },{ # Nook
        'regex' : r'(nook)[\w ]+build\/(\w+)',                                            
        'props' : {'vendor': None, 'model': None, 'type': 'tablet'}, 
    },{ # Dell Streak
        'regex' : r'(dell) (strea[kpr\d ]*[\dko])',
        'props' : {'vendor': None, 'model': None, 'type': 'tablet'}, 
    },{ # Le Pan Tablets
        'regex' : r'(le[- ]+pan)[- ]+(\w{1,9}) bui',
        'props' : {'vendor': None, 'model': None, 'type': 'tablet'}, 
    },{ # Trinity Tablets
        'regex' : r'(trinity)[- ]*(t\d{3}) bui',
        'props' : {'vendor': None, 'model': None, 'type': 'tablet'}, 
    },{ # Gigaset Tablets
        'regex' : r'(gigaset)[- ]+(q\w{1,9}) bui',
        'props' : {'vendor': None, 'model': None, 'type': 'tablet'}, 
    },{ # Vodafone
        'regex' : r'(vodafone) ([\w ]+)(?:\)| bui)',
        'props' : {'vendor': None, 'model': None, 'type': 'tablet'}, 
    },{ # Surface Duo
        'regex' : r'(surface duo)',
        'props' : {'model': None, 'vendor': 'Microsoft', 'type': 'tablet'}, 
    },{ # Fairphone
        'regex' : r'droid [\d\.]+; (fp\du?)(?: b|\))',
        'props' : {'model': None, 'vendor': 'Fairphone', 'type': 'mobile'}, 
    },{ # AT&T
        'regex' : r'(u304aa)',                                                    
        'props' : {'model': None, 'vendor': 'AT&T', 'type': 'mobile'},  
    },{ # Siemens
        'regex' : r'\bsie-(\w*)',                                                 
        'props' : {'model': None, 'vendor': 'Siemens', 'type': 'mobile'}, 
    },{ # RCA Tablets
        'regex' : r'\b(rct\w+) b',                                                
        'props' : {'model': None, 'vendor': 'RCA', 'type': 'tablet'}, 
    },{ # Dell Venue Tablets
        'regex' : r'\b(venue[\d ]{2,7}) b',                                       
        'props' : {'model': None, 'vendor': 'Dell', 'type': 'tablet'}, 
    },{ # Verizon Tablet
        'regex' : r'\b(q(?:mv|ta)\w+) b',                                         
        'props' : {'model': None, 'vendor': 'Verizon', 'type': 'tablet'}, 
    },{ # Barnes & Noble Tablet
        'regex' : r'\b(?:barnes[& ]+noble |bn[rt])([\w\+ ]*) b',                  
        'props' : {'model': None, 'vendor': 'Barnes & Noble', 'type': 'tablet'}, 
    },{
        'regex' : r'\b(tm\d{3}\w+) b',
        'props' : {'model': None, 'vendor': 'NuVision', 'type': 'tablet'}, 
    },{ # ZTE K Series Tablet
        'regex' : r'\b(k88) b',                                                   
        'props' : {'model': None, 'vendor': 'ZTE', 'type': 'tablet'}, 
    },{ # ZTE Nubia
        'regex' : r'\b(nx\d{3}j) b',                                              
        'props' : {'model': None, 'vendor': 'ZTE', 'type': 'mobile'},  
    },{ # Swiss GEN Mobile
        'regex' : r'\b(gen\d{3}) b.+49h',                                         
        'props' : {'model': None, 'vendor': 'Swiss', 'type': 'mobile'},  
    },{ # Swiss ZUR Tablet
        'regex' : r'\b(zur\d{3}) b',                                              
        'props' : {'model': None, 'vendor': 'Swiss', 'type': 'tablet'}, 
    },{ # Zeki Tablets
        'regex' : r'\b((zeki)?tb.*\b) b',                                         
        'props' : {'model': None, 'vendor': 'Zeki', 'type': 'tablet'}, 
    },{ # Dragon Touch Tablet
        'regex' : r'\b([yr]\d{2}) b',                                             
        'props' : {'vendor': 'Dragon Touch', 'model': None, 'type': 'tablet'}, 
    },{ # Dragon Touch Tablet
        'regex' : r'\b(dragon[- ]+touch |dt)(\w{5}) b',                           
        'props' : {'vendor': 'Dragon Touch', 'model': None, 'type': 'tablet'}, 
    },{ # Insignia Tablets
        'regex' : r'\b(ns-?\w{0,9}) b',                                           
        'props' : {'model': None, 'vendor': 'Insignia', 'type': 'tablet'}, 
    },{ # NextBook Tablets
        'regex' : r'\b((nxa|next)-?\w{0,9}) b',                                   
        'props' : {'model': None, 'vendor': 'NextBook', 'type': 'tablet'}, 
    },{ # Voice Xtreme Phones
        'regex' : r'\b(xtreme\_)?(v(1[045]|2[015]|[3469]0|7[05])) b',             
        'props' : {'vendor': 'Voice', 'model': None, 'type': 'mobile'}, 
    },{ # LvTel Phones
        'regex' : r'\b(lvtel\-)?(v1[12]) b',                                      
        'props' : {'vendor': 'LvTel', 'model': None, 'type': 'mobile'}, 
    },{ # Essential PH-1
        'regex' : r'\b(ph-1) ',                                                   
        'props' : {'model': None, 'vendor': 'Essential', 'type': 'mobile'}, 
    },{ # Envizen Tablets
        'regex' : r'\b(v(100md|700na|7011|917g).*\b) b',                          
        'props' : {'model': None, 'vendor': 'Envizen', 'type': 'tablet'}, 
    },{ # MachSpeed Tablets
        'regex' : r'\b(trio[-\w\. ]+) b',                                         
        'props' : {'model': None, 'vendor': 'MachSpeed', 'type': 'tablet'}, 
    },{ # Rotor Tablets
        'regex' : r'\btu_(1491) b',                                               
        'props' : {'model': None, 'vendor': 'Rotor', 'type': 'tablet'}, 
    },{ # Nvidia Shield Tablets
        'regex' : r'(shield[\w ]+) b',                                            
        'props' : {'model': None, 'vendor': 'Nvidia', 'type': 'tablet'}, 
    },{ # Sprint Phones
        'regex' : r'(sprint) (\w+)',
        'props' : {'vendor': None, 'model': None, 'type': 'mobile'}, 
    },{ # Microsoft Kin
        'regex' : r'(kin\.[onetw]{3})',
        'props' : {
            'model' : lambda s: re.sub(r'\.', ' ', s),
            'vendor': 'Microsoft',
            'type'  : 'mobile'}
    },{ # Zebra
        'regex' : r'droid.+; (cc6666?|et5[16]|mc[239][23]x?|vc8[03]x?)\)',
        'props' : {'model': None, 'vendor': 'Zebra', 'type': 'tablet'}, 
    },{
        'regex' : r'droid.+; (ec30|ps20|tc[2-8]\d[kx])\)', 
        'props' : {'model': None, 'vendor': 'Zebra', 'type': 'mobile'}, 
    },{ # Ouya
        'regex' : r'(ouya)',
        'props' : {'vendor': None, 'model': None, 'type': 'console'},  
    },{ # Nintendo
        'regex' : r'(nintendo) ([wids3utch]+)',
        'props' : {'vendor': None, 'model': None, 'type': 'console'},  
    },{ # Nvidia
        'regex' : r'droid.+; (shield) bui',
        'props' : {'model': None, 'vendor': 'Nvidia', 'type': 'console'}, 
    },{ # Playstation
        'regex' : r'(playstation [345portablevi]+)',
        'props' : {'model': None, 'vendor': 'Sony', 'type': 'console'}, 
    },{ # Microsoft Xbox
        'regex' : r'\b(xbox(?: one)?(?!; xbox))[\); ]',
        'props' : {'model': None, 'vendor': 'Microsoft', 'type': 'console'},  
    },{ # Samsung SmartTV
        'regex' : r'smart-tv.+(samsung)',
        'props' : {'vendor': None, 'type': 'smarttv'}, 
    },{
        'regex' : r'hbbtv.+maple;(\d+)',
        'props' : {
            'model' : lambda s: re.sub(r'^', 'SmartTV', s),
            'vendor': 'Samsung',
            'type'  : 'smarttv'}
    },{ # 'LG' SmartTV
        'regex' : r'(nux; netcast.+smarttv|lg (netcast\.tv-201\d|android tv))',
        'props' : {'vendor': 'LG', 'type': 'smarttv'},  
    },{ # Apple TV
        'regex' : r'(apple) ?tv',
        'props' : {'vendor': None, 'model': 'Apple TV', 'type': 'smarttv'},  
    },{ # Google Chromecast
        'regex' : r'crkey',
        'props' : {'model': 'Chromecast', 'vendor': 'Google', 'type': 'smarttv'},  
    },{ # Fire TV
        'regex' : r'droid.+aft(\w)( bui|\))',
        'props' : {'model': None, 'vendor': 'Amazon', 'type': 'smarttv'},  
    },{ # Sharp
        'regex' : r'\(dtv[\);].+(aquos)',
        'props' : {'model': None, 'vendor': 'Sharp', 'type': 'smarttv'},  
    },{ # Roku
        'regex' : r'\b(roku)[\dx]*[\)\/]((?:dvp-)?[\d\.]*)',
        'props' : {
            'vendor': lambda s: re.sub(r'\s\s*$', EMPTY, re.sub(r'^\s\s*', EMPTY, s)), 
            'model' : lambda s: re.sub(r'\s\s*$', EMPTY, re.sub(r'^\s\s*', EMPTY, s)),  
            'type'  : 'smarttv'
            },  
    },{ # HbbTV devices
        'regex' : r'hbbtv\/\d+\.\d+\.\d+ +\([\w ]*; *(\w[^;]*);([^;]*)',
        'props' : {
            'vendor': lambda s: re.sub(r'\s\s*$', EMPTY, re.sub(r'^\s\s*', EMPTY, s)), 
            'model' : lambda s: re.sub(r'\s\s*$', EMPTY, re.sub(r'^\s\s*', EMPTY, s)), 
            'type'  : 'smarttv'
            },  
    },{ # SmartTV from Unidentified Vendors
        'regex' : r'\b(android tv|smart[- ]?tv|opera tv|tv; rv:)\b',              
        'props' : {'type': 'smarttv'},  
    },{ # Pebble
        'regex' : r'((pebble))app',                                               
        'props' : {'vendor': None, 'model': None, 'type': 'wearable'}, 
    },{ # Google Glass
        'regex' : r'droid.+; (glass) \d',                                         
        'props' : {'model': None, 'vendor': 'Google', 'type': 'wearable'},  
    },{
        'regex' : r'droid.+; (wt63?0{2,3})\)',
        'props' : {'model': None, 'vendor': 'Zebra', 'type': 'wearable'},  
    },{ # Oculus Quest
        'regex' : r'(quest( 2)?)',                                                
        'props' : {'model': None, 'vendor': 'Facebook', 'type': 'wearable'},  
    },{ # Tesla
        'regex' : r'(tesla)(?: qtcarbrowser|\/[-\w\.]+)',                         
        'props' : {'vendor': None, 'type': 'embedded'},  
    },{ # Android Phones from Unidentified Vendors
        'regex' : r'droid .+?; ([^;]+?)(?: bui|\) applew).+? mobile safari',      
        'props' : {'model': None, 'type': 'mobile'},  
    },{ # Android Tablets from Unidentified Vendors
        'regex' : r'droid .+?; ([^;]+?)(?: bui|\) applew).+?(?! mobile) safari',  
        'props' : {'model': None, 'type': 'tablet'},  
    },{ # Unidentifiable Tablet
        'regex' : r'\b((tablet|tab)[;\/]|focus\/\d(?!.+mobile))',                 
        'props' : {'type': 'tablet'},  
    },{ # Unidentifiable Mobile
        'regex' : r'(phone|mobile(?:[;\/]| safari)|pda(?=.+windows ce))',         
        'props' : {'type': 'mobile'},  
    },{ # Generic Android Device
        'regex' : r'(android[-\w\. ]{0,9});.+buil',                                
        'props' : {'model': None, 'vendor': 'Generic'}
    }
]

ENGINE = [
    { # EdgeHTML
        'regex' : r'windows.+ edge\/([\w\.]+)',                           
        'props' : {'version': None, 'name': 'EdgeHTML'}, 
    },{ # Blink
        'regex' : r'webkit\/537\.36.+chrome\/(?!27)([\w\.]+)',            
        'props' : {'version': None, 'name': 'Blink'}, 
    },{ # Presto
        'regex' : r'(presto)\/([\w\.]+)',                                         
        'props' : {'name': None, 'version': None}, 
    },{ # WebKit/Trident/NetFront/NetSurf/Amaya/Lynx/w3m/Goanna
        'regex' : r'(webkit|trident|netfront|netsurf|amaya|lynx|w3m|goanna)\/([\w\.]+)',  
        'props' : {'name': None, 'version': None}, 
    },{ # Flow
        'regex' : r'ekioh(flow)\/([\w\.]+)',                                      
        'props' : {'name': None, 'version': None}, 
    },{ # KHTML/Tasman/Links
        'regex' : r'(khtml|tasman|links)[\/ ]\(?([\w\.]+)',                       
        'props' : {'name': None, 'version': None}, 
    },{ # iCab 
        'regex' : r'(icab)[\/ ]([23]\.[\d\.]+)',                                   
        'props' : {'name': None, 'version': None}, 
    },{ # Gecko
        'regex' : r'rv\:([\w\.]{1,9})\b.+(gecko)',                        
        'props' : {'version': None, 'name': None}, 
    }
]

OS = [
    { # Windows (iTunes)
        'regex' : r'microsoft (windows) (vista|xp)',                            
        'props' : {'name': None, 'version': None}, 
    },{ # Windows RT
        'regex' : r'(windows) nt 6\.2; (arm)',                                    
        'props' : {
            'name'   : None, 
            'version': lambda s: strMapper(s, WINDOWS_VERSIONS)
        }, 
    },{ # Windows Phone
        'regex' : r'(windows (?:phone(?: os)?|mobile))[\/ ]?([\d\.\w ]*)',        
        'props' : {
            'name'   : None, 
            'version': lambda s: strMapper(s, WINDOWS_VERSIONS)
        }, 
    },{
        'regex' : r'(windows)[\/ ]?([ntce\d\. ]+\w)(?!.+xbox)',
        'props' : {
            'name'   : None, 
            'version': lambda s: strMapper(s, WINDOWS_VERSIONS)
        }, 
    },{
        'regex' : r'(win(?=3|9|n)|win 9x )([nt\d\.]+)', 
        'props' : {
            'name'   : 'Windows', 
            'version': lambda s: strMapper(s, WINDOWS_VERSIONS)
        }, 
    },{ # iOS
        'regex' : r'ip[honead]{2,4}\b(?:.*os ([\w]+) like mac|; opera)',          
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
    },{ # Mac OS
        'regex' : r'(mac os x) ?([\w\. ]*)',                                    
        'props' : {
            'name'   : 'Mac OS',
            'version': lambda s: re.sub('_', '.', s)
        },
    },{ # Mac OS
        'regex' : r'(macintosh|mac_powerpc\b)(?!.+haiku)', 
        'props' : {
            'name'   : 'Mac OS',
            'version': lambda s: re.sub('_', '.', s)
        },
    },{ # Android-x86
        'regex' : r'droid ([\w\.]+)\b.+(android[- ]x86)',
        'props' : {'version': None, 'name': None}, 
    },{ # Android/WebOS/QNX/Bada/RIM/Maemo/MeeGo/Sailfish OS
        'regex' : r'(android|webos|qnx|bada|rim tablet os|maemo|meego|sailfish)[-\/ ]?([\w\.]*)',  
        'props' : {'name': None, 'version': None}, 
    },{ # Blackberry
        'regex' : r'(blackberry)\w*\/([\w\.]*)',
        'props' : {'name': None, 'version': None}, 
    },{ # Tizen/KaiOS
        'regex' : r'(tizen|kaios)[\/ ]([\w\.]+)',
        'props' : {'name': None, 'version': None}, 
    },{ # Series 40
        'regex' : r'\((series40);',
        'props' : {'name': None, 'version': None},  
    },{ # BlackBerry 10
        'regex' : r'\(bb(10);',
        'props' : {'version': None, 'name': 'BlackBerry'}, 
    },{ # Symbian
        'regex' : r'(?:symbian ?os|symbos|s60(?=;)|series60)[-\/ ]?([\w\.]*)',
        'props' : {'version': None, 'name': 'Symbian'}, 
    },{ # Firefox OS
        'regex' : r'mozilla\/[\d\.]+ \((?:mobile|tablet|tv|mobile; [\w ]+); rv:.+ gecko\/([\w\.]+)',
        'props' : {'version': None, 'name': 'Firefox OS'}, 
    },{ # WebOS
        'regex' : r'web0s;.+rt(tv)',
        'props' : {'version': None, 'name': 'webOS'}, 
    },{ # WebOS
        'regex' : r'\b(?:hp)?wos(?:browser)?\/([\w\.]+)',
        'props' : {'version': None, 'name': 'webOS'}, 
    },{ # Google Chromecast
        'regex' : r'crkey\/([\d\.]+)',
        'props' : {'version': None, 'name': 'Chromecast'}, 
    },{ # Chromium OS
        'regex' : r'(cros) [\w]+ ([\w\.]+\w)',
        'props' : {'name': 'Chromium OS', 'version': None}, 
    },{ # Nintendo/Playstation
        'regex' : r'(nintendo|playstation) ([wids345portablevuch]+)',
        'props' : {'name': None, 'version': None},
    },{ # Microsoft Xbox (360, One, X, S, Series X, Series S)
        'regex' : r'(xbox); +xbox ([^\);]+)',
        'props' : {'name': None, 'version': None},
    },{ # Joli/Palm
        'regex' : r'\b(joli|palm)\b ?(?:os)?\/?([\w\.]*)',
        'props' : {'name': None, 'version': None},
    },{ # Mint
        'regex' : r'(mint)[\/\(\) ]?(\w*)', 
        'props' : {'name': None, 'version': None},
    },{ # Mageia/VectorLinux
        'regex' : r'(mageia|vectorlinux)[; ]',
        'props' : {'name': None, 'version': None},
    },{ 
        'regex' : r'([kxln]?ubuntu|debian|suse|opensuse|gentoo|arch(?= linux)|slackware|fedora|mandriva|centos|pclinuxos|red ?hat|zenwalk|linpus|raspbian|plan 9|minix|risc os|contiki|deepin|manjaro|elementary os|sabayon|linspire)(?: gnu\/linux)?(?: enterprise)?(?:[- ]linux)?(?:-gnu)?[-\/ ]?(?!chrom|package)([-\w\.]*)',  # Ubuntu/Debian/SUSE/Gentoo/Arch/Slackware/Fedora/Mandriva/CentOS/PCLinuxOS/RedHat/Zenwalk/Linpus/Raspbian/Plan9/Minix/RISCOS/Contiki/Deepin/Manjaro/elementary/Sabayon/Linspire
        'props' : {'name': None, 'version': None},
    },{ # Hurd/Linux
        'regex' : r'(hurd|linux) ?([\w\.]*)',
        'props' : {'name': None, 'version': None},
    },{ # GNU
        'regex' : r'(gnu) ?([\w\.]*)',                                            
        'props' : {'name': None, 'version': None},
    },{ # FreeBSD/NetBSD/OpenBSD/PC-BSD/GhostBSD/DragonFly
        'regex' : r'\b([-frentopcghs]{0,5}bsd|dragonfly)[\/ ]?(?!amd|[ix346]{1,2}86)([\w\.]*)',  
        'props' : {'name': None, 'version': None},
    },{ # Haiku
        'regex' : r'(haiku) (\w+)',
        'props' : {'name': None, 'version': None},
    },{ # Solaris
        'regex' : r'(sunos) ?([\w\.\d]*)',
        'props' : {'name': 'Solaris', 'version': None}, 
    },{ # Solaris
        'regex' : r'((?:open)?solaris)[-\/ ]?([\w\.]*)',
        'props' : {'name': None, 'version': None},
    },{ # AIX
        'regex' : r'(aix) ((\d)(?=\.|\)| )[\w\.])*',
        'props' : {'name': None, 'version': None},
    },{ # BeOS/OS2/AmigaOS/MorphOS/OpenVMS/Fuchsia/HP-UX
        'regex' : r'\b(beos|os\/2|amigaos|morphos|openvms|fuchsia|hp-ux)',
        'props' : {'name': None, 'version': None},
    },{ # UNIX
        'regex' : r'(unix) ?([\w\.]*)',
        'props' : {'name': None, 'version': None},
    }
]

