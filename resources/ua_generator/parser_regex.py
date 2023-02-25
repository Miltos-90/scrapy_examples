import re
from parser_utils import str_mapper, lowerize, trim
from parser_utils import EMPTY


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



REGEXES = {
    'browser': [
        [r'\b(?:crmo|crios)\/([\w\.]+)'],  # Chrome for Android/iOS
        ['version', ['name', 'Chrome']], 
        [r'edg(?:e|ios|a)?\/([\w\.]+)'], # # Microsoft Edge
        ['version', ['name', 'Edge']], [
            # Presto based
            r'(opera mini)\/([-\w\.]+)',  # Opera Mini
            r'(opera [mobiletab]{3,6})\b.+version\/([-\w\.]+)',  # Opera Mobi/Tablet
            r'(opera)(?:.+version\/|[\/ ]+)([\w\.]+)'  # Opera
        ], ['name', 'version'], [
            r'opios[\/ ]+([\w\.]+)'  # Opera mini on iphone >= 8.0
        ], ['version', ['name', 'Opera' + ' Mini']], [
            r'\bopr\/([\w\.]+)'  # Opera Webkit
        ], ['version', ['name', 'Opera']], [

            # Mixed
            r'(kindle)\/([\w\.]+)',  # Kindle
            r'(lunascape|maxthon|netfront|jasmine|blazer)[\/ ]?([\w\.]*)',  # Lunascape/Maxthon/Netfront/Jasmine/Blazer

            # Trident based
            r'(avant |iemobile|slim)(?:browser)?[\/ ]?([\w\.]*)',  # Avant/IEMobile/SlimBrowser
            r'(ba?idubrowser)[\/ ]?([\w\.]+)',  # Baidu Browser
            r'(?:ms|\()(ie) ([\w\.]+)',  # Internet Explorer

            # Webkit/KHTML based
            r'(flock|rockmelt|midori|epiphany|silk|skyfire|ovibrowser|bolt|iron|vivaldi|iridium|phantomjs|bowser|quark|qupzilla|falkon|rekonq|puffin|brave|whale|qqbrowserlite|qq)\/([-\w\.]+)',  # Rekonq/Puffin/Brave/Whale/QQBrowserLite/QQ, aka ShouQ
            r'(weibo)__([\d\.]+)'  # Weibo
        ], ['name', 'version'], [
            r'(?:\buc? ?browser|(?:juc.+)ucweb)[\/ ]?([\w\.]+)'  # UCBrowser
        ], ['version', ['name', 'UC' + 'Browser']], [
            r'\bqbcore\/([\w\.]+)'  # WeChat Desktop for Windows Built-in Browser
        ], ['version', ['name', 'WeChat(Win) Desktop']], [
            r'micromessenger\/([\w\.]+)'  # WeChat
        ], ['version', ['name', 'WeChat']], [
            r'konqueror\/([\w\.]+)'  # Konqueror
        ], ['version', ['name', 'Konqueror']], [
            r'trident.+rv[: ]([\w\.]{1,9})\b.+like gecko'  # IE11
        ], ['version', ['name', 'IE']], [
            r'yabrowser\/([\w\.]+)'  # Yandex
        ], ['version', ['name', 'Yandex']], [
            r'(avast|avg)\/([\w\.]+)'  # Avast/AVG Secure Browser
        ], [['name', r'(.+)', '$1 Secure ' + 'Browser'], 'version'], [
            r'\bfocus\/([\w\.]+)'  # Firefox Focus
        ], ['version', ['name', 'Firefox' + ' Focus']], [
            r'\bopt\/([\w\.]+)'  # Opera Touch
        ], ['version', ['name', 'Opera' + ' Touch']], [
            r'coc_coc\w+\/([\w\.]+)'  # Coc Coc Browser
        ], ['version', ['name', 'Coc Coc']], [
            r'dolfin\/([\w\.]+)'  # Dolphin
        ], ['version', ['name', 'Dolphin']], [
            r'coast\/([\w\.]+)'  # Opera Coast
        ], ['version', ['name', 'Opera' + ' Coast']], [
            r'miuibrowser\/([\w\.]+)'  # MIUI Browser
        ], ['version', ['name', 'MIUI ' + 'Browser']], [
            r'fxios\/([-\w\.]+)'  # Firefox for iOS
        ], ['version', ['name', 'Firefox']], [
            r'\bqihu|(qi?ho?o?|360)browser'  # 360
        ], [['name', '360 ' + 'Browser']], [
            r'(oculus|samsung|sailfish)browser\/([\w\.]+)'  # Oculus/Samsung/Sailfish Browser
        ], [['name', r'(.+)', '$1 ' + 'Browser'], 'version'], [
            r'(comodo_dragon)\/([\w\.]+)'  # Comodo Dragon
        ], [['name', r'_', ' '], 'version'], [
            r'(electron)\/([\w\.]+) safari',  # Electron-based App
            r'(tesla)(?: qtcarbrowser|\/(20\d\d\.[-\w\.]+))',  # Tesla
            r'm?(qqbrowser|baiduboxapp|2345Explorer)[\/ ]?([\w\.]+)'  # QQBrowser/Baidu App/2345 Browser
        ], ['name', 'version'], [
            r'(metasr)[\/ ]?([\w\.]+)',  # SouGouBrowser
            r'(lbbrowser)'  # LieBao Browser
        ], ['name'], [

            # WebView
            r'((?:fban\/fbios|fb_iab\/fb4a)(?!.+fbav)|;fbav\/([\w\.]+);)'  # Facebook App for iOS & Android
        ], [['name', 'Facebook'], 'version'], [
            r'safari (line)\/([\w\.]+)',  # Line App for iOS
            r'\b(line)\/([\w\.]+)\/iab',  # Line App for Android
            r'(chromium|instagram)[\/ ]([-\w\.]+)'  # Chromium/Instagram
        ], ['name', 'version'], [
            r'\bgsa\/([\w\.]+) .*safari\/'  # Google Search Appliance on iOS
        ], ['version', ['name', 'GSA']], [
            r'headlesschrome(?:\/([\w\.]+)| )'  # Chrome Headless
        ], ['version', ['name', 'Chrome' + ' Headless']], [
            r' wv\).+(chrome)\/([\w\.]+)'  # Chrome WebView
        ], [['name', 'Chrome' + ' WebView'], 'version'], [
            r'droid.+ version\/([\w\.]+)\b.+(?:mobile safari|safari)'  # Android Browser
        ], ['version', ['name', 'Android ' + 'Browser']], [
            r'(chrome|omniweb|arora|[tizenoka]{5} ?browser)\/v?([\w\.]+)'  # Chrome/OmniWeb/Arora/Tizen/Nokia
        ], ['name', 'version'], [
            r'version\/([\w\.]+) .*mobile\/\w+ (safari)'  # Mobile Safari
        ], ['version', ['name', 'Mobile Safari']], [
            r'version\/([\w\.]+) .*(mobile ?safari|safari)'  # Safari & Safari Mobile
        ], ['version', 'name'], [
            r'webkit.+?(mobile ?safari|safari)(\/[\w\.]+)'  # Safari < 3.0
        ], ['name', ['version', str_mapper, OLD_SAFARI_MAP]], [
            r'(webkit|khtml)\/([\w\.]+)'
        ], ['name', 'version'], [

            # Gecko based
            r'(navigator|netscape\d?)\/([-\w\.]+)'  # Netscape
        ], [['name', 'Netscape'], 'version'], [
            r'mobile vr; rv:([\w\.]+)\).+firefox'  # Firefox Reality
        ], ['version', ['name', 'Firefox' + ' Reality']], [
            r'ekiohf.+(flow)\/([\w\.]+)',  # Flow
            r'(swiftfox)',  # Swiftfox
            r'(icedragon|iceweasel|camino|chimera|fennec|maemo browser|minimo|conkeror|klar)[\/ ]?([\w\.\+]+)',  # IceDragon/Iceweasel/Camino/Chimera/Fennec/Maemo/Minimo/Conkeror/Klar
            r'(seamonkey|k-meleon|icecat|iceape|firebird|phoenix|palemoon|basilisk|waterfox)\/([-\w\.]+)$',  # Firefox/SeaMonkey/K-Meleon/IceCat/IceApe/Firebird/Phoenix
            r'(firefox)\/([\w\.]+)',  # Other Firefox-based
            r'(mozilla)\/([\w\.]+) .+rv\:.+gecko\/\d+',  # Mozilla

            # Other
            r'(polaris|lynx|dillo|icab|doris|amaya|w3m|netsurf|sleipnir|obigo|mosaic|(?:go|ice|up)[\. ]?browser)[-\/ ]?v?([\w\.]+)',  # Polaris/Lynx/Dillo/iCab/Doris/Amaya/w3m/NetSurf/Sleipnir/Obigo/Mosaic/Go/ICE/UP.Browser
            r'(links) \(([\w\.]+)'  # Links
        ], ['name', 'version']
    
    ],

    'cpu': [[
        r'(?:(amd|x(?:(?:86|64)[-_])?|wow|win)64)[;\)]'  # AMD64 (x64)
    ], [['architecture', 'amd64']], [
        r'(ia32(?=;))'  # IA32 (quicktime)
    ], [['architecture', lowerize]], [
        r'((?:i[346]|x)86)[;\)]'  # IA32 (x86)
    ], [['architecture', 'ia32']], [
        r'\b(aarch64|arm(v?8e?l?|_?64))\b'  # ARM64
    ], [['architecture', 'arm64']], [
        r'\b(arm(?:v[67])?ht?n?[fl]p?)\b'  # ARMHF
    ], [['architecture', 'armhf']], [
        r'windows (ce|mobile); ppc;'  # PocketPC mistakenly identified as PowerPC
    ], [['architecture', 'arm']], [
        r'((?:ppc|powerpc)(?:64)?)(?: mac|;|\))'  # PowerPC
    ], [['architecture', r'ower', EMPTY, lowerize]], [
        r'(sun4\w)[;\)]'  # SPARC
    ], [['architecture', 'sparc']], [
        r'((?:avr32|ia64(?=;))|68k(?=\))|\barm(?=v(?:[1-7]|[5-7]1)l?|;|eabi)|(?=atmel )avr|(?:irix|mips|sparc)(?:64)?\b|pa-risc)'  # IA64, 68K, ARM/64, AVR/32, IRIX/64, MIPS/64, SPARC/64, PA-RISC
    ], [['architecture', lowerize]]],

    'device': [[
        # Samsung
        r'\b(sch-i[89]0\d|shw-m380s|sm-[pt]\w{2,4}|gt-[pn]\d{2,4}|sgh-t8[56]9|nexus 10)'
    ], ['model', ['vendor', 'Samsung'], ['type', 'tablet']], [
        r'\b((?:s[cgp]h|gt|sm)-\w+|galaxy nexus)',
        r'samsung[- ]([-\w]+)',
        r'sec-(sgh\w+)'
    ], ['model', ['vendor', 'Samsung'], ['type', 'mobile']], [

        # Apple
        r'\((ip(?:hone|od)[\w ]*);'  # iPod/iPhone
    ], ['model', ['vendor', 'Apple'], ['type', 'mobile']], [
        r'\((ipad);[-\w\),; ]+apple',  # iPad
        r'applecoremedia\/[\w\.]+ \((ipad)',
        r'\b(ipad)\d\d?,\d\d?[;\]].+ios'
    ], ['model', ['vendor', 'Apple'], ['type', 'tablet']], [

        # Huawei
        r'\b((?:ag[rs][23]?|bah2?|sht?|btv)-a?[lw]\d{2})\b(?!.+d\/s)'
    ], ['model', ['vendor', 'Huawei'], ['type', 'tablet']], [
        r'(?:huawei|honor)([-\w ]+)[;\)]',
        r'\b(nexus 6p|\w{2,4}-[atu]?[ln][01259x][012359][an]?)\b(?!.+d\/s)'
    ], ['model', ['vendor', 'Huawei'], ['type', 'mobile']], [

        # Xiaomi
        r'\b(poco[\w ]+)(?: bui|\))',  # Xiaomi POCO
        r'\b; (\w+) build\/hm\1',  # Xiaomi Hongmi 'numeric' models
        r'\b(hm[-_ ]?note?[_ ]?(?:\d\w)?) bui',  # Xiaomi Hongmi
        r'\b(redmi[\-_ ]?(?:note|k)?[\w_ ]+)(?: bui|\))',  # Xiaomi Redmi
        r'\b(mi[-_ ]?(?:a\d|one|one[_ ]plus|note lte|max)?[_ ]?(?:\d?\w?)[_ ]?(?:plus|se|lite)?)(?: bui|\))'  # Xiaomi Mi
    ], [['model', '_', ' '], ['vendor', 'Xiaomi'], ['type', 'mobile']], [
        r'\b(mi[-_ ]?(?:pad)(?:[\w_ ]+))(?: bui|\))'  # Mi Pad tablets
    ], [['model', '_', ' '], ['vendor', 'Xiaomi'], ['type', 'tablet']], [

        # OPPO
        r'; (\w+) bui.+ oppo',
        r'\b(cph[12]\d{3}|p(?:af|c[al]|d\w|e[ar])[mt]\d0|x9007|a101op)\b'
    ], ['model', ['vendor', 'OPPO'], ['type', 'mobile']], [

        # Vivo
        r'vivo (\w+)(?: bui|\))',
        r'\b(v[12]\d{3}\w?[at])(?: bui|;)'
    ], ['model', ['vendor', 'Vivo'], ['type', 'mobile']], [

        # Realme
        r'\b(rmx[12]\d{3})(?: bui|;|\))'
    ], ['model', ['vendor', 'Realme'], ['type', 'mobile']], [

        # Motorola
        r'\b(milestone|droid(?:[2-4x]| (?:bionic|x2|pro|razr))?:?( 4g)?)\b[\w ]+build\/',
        r'\bmot(?:orola)?[- ](\w*)',
        r'((?:moto[\w\(\) ]+|xt\d{3,4}|nexus 6)(?= bui|\)))'
    ], ['model', ['vendor', 'Motorola'], ['type', 'mobile']], [
        r'\b(mz60\d|xoom[2 ]{0,2}) build\/'
    ], ['model', ['vendor', 'Motorola'], ['type', 'tablet']], [

        # 'LG'
        r'((?=lg)?[vl]k\-?\d{3}) bui| 3\.[-\w; ]{10}lg?-([06cv9]{3,4})'
    ], ['model', ['vendor', 'LG'], ['type', 'tablet']], [
        r'(lm(?:-?f100[nv]?|-[\w\.]+)(?= bui|\))|nexus [45])',
        r'\blg[-e;\/ ]+((?!browser|netcast|android tv)\w+)',
        r'\blg-?([\d\w]+) bui'
    ], ['model', ['vendor', 'LG'], ['type', 'mobile']], [

        # Lenovo
        r'(ideatab[-\w ]+)',
        r'lenovo ?(s[56]000[-\w]+|tab(?:[\w ]+)|yt[-\d\w]{6}|tb[-\d\w]{6})'
    ], ['model', ['vendor', 'Lenovo'], ['type', 'tablet']], [

        # Nokia
        r'(?:maemo|nokia).*(n900|lumia \d+)',
        r'nokia[-_ ]?([-\w\.]*)'
    ], [['model', '_', ' '], ['vendor', 'Nokia'], ['type', 'mobile']], [

        # Google
        r'(pixel c)\b'  # Google Pixel C
    ], ['model', ['vendor', 'Google'], ['type', 'tablet']], [
        r'droid.+; (pixel[\daxl ]{0,6})(?: bui|\))'  # Google Pixel
    ], ['model', ['vendor', 'Google'], ['type', 'mobile']], [

        # Sony
        r'droid.+ ([c-g]\d{4}|so[-gl]\w+|xq-a\w[4-7][12])(?= bui|\).+chrome\/(?![1-6]{0,1}\d\.))'
    ], ['model', ['vendor', 'Sony'], ['type', 'mobile']], [
        r'sony tablet [ps]',
        r'\b(?:sony)?sgp\w+(?: bui|\))'
    ], [['model', 'Xperia Tablet'], ['vendor', 'Sony'], ['type', 'tablet']], [

        # OnePlus
        r' (kb2005|in20[12]5|be20[12][59])\b',
        r'(?:one)?(?:plus)? (a\d0\d\d)(?: b|\))'
    ], ['model', ['vendor', 'OnePlus'], ['type', 'mobile']], [

        # Amazon
        r'(alexa)webm',
        r'(kf[a-z]{2}wi)( bui|\))',  # Kindle Fire without Silk
        r'(kf[a-z]+)( bui|\)).+silk\/'  # Kindle Fire HD
    ], ['model', ['vendor', 'Amazon'], ['type', 'tablet']], [
        r'((?:sd|kf)[0349hijorstuw]+)( bui|\)).+silk\/'  # Fire Phone
    ], [['model', '(.+)', 'Fire Phone $1'], ['vendor', 'Amazon'], ['type', 'mobile']], [

        # BlackBerry
        r'(playbook);[-\w\),; ]+(rim)'  # BlackBerry PlayBook
    ], ['model', 'vendor', ['type', 'tablet']], [
        r'\b((?:bb[a-f]|st[hv])100-\d)',
        r'\(bb10; (\w+)'  # BlackBerry 10
    ], ['model', ['vendor', 'BlackBerry'], ['type', 'mobile']], [

        # Asus
        r'(?:\b|asus_)(transfo[prime ]{4,10} \w+|eeepc|slider \w+|nexus 7|padfone|p00[cj])'
    ], ['model', ['vendor', 'ASUS'], ['type', 'tablet']], [
        r' (z[bes]6[027][012][km][ls]|zenfone \d\w?)\b'
    ], ['model', ['vendor', 'ASUS'], ['type', 'mobile']], [

        # HTC
        r'(nexus 9)'  # HTC Nexus 9
    ], ['model', ['vendor', 'HTC'], ['type', 'tablet']], [
        r'(htc)[-;_ ]{1,2}([\w ]+(?=\)| bui)|\w+)',  # HTC

        # ZTE
        r'(zte)[- ]([\w ]+?)(?: bui|\/|\))',
        r'(alcatel|geeksphone|nexian|panasonic|sony)[-_ ]?([-\w]*)'  # Alcatel/GeeksPhone/Nexian/Panasonic/Sony
    ], ['vendor', ['model', '_', ' '], ['type', 'mobile']], [

        # Acer
        r'droid.+; ([ab][1-7]-?[0178a]\d\d?)'
    ], ['model', ['vendor', 'Acer'], ['type', 'tablet']], [

        # Meizu
        r'droid.+; (m[1-5] note) bui',
        r'\bmz-([-\w]{2,})'
    ], ['model', ['vendor', 'Meizu'], ['type', 'mobile']], [

        # Sharp
        r'\b(sh-?[altvz]?\d\d[a-ekm]?)'
    ], ['model', ['vendor', 'Sharp'], ['type', 'mobile']], [

        # Mixed
        r'(blackberry|benq|palm(?=\-)|sonyericsson|acer|asus|dell|meizu|motorola|polytron)[-_ ]?([-\w]*)',  # BlackBerry/BenQ/Palm/Sony-Ericsson/Acer/Asus/Dell/Meizu/Motorola/Polytron
        r'(hp) ([\w ]+\w)',  # HP iPAQ
        r'(asus)-?(\w+)',  # Asus
        r'(microsoft); (lumia[\w ]+)',  # Microsoft Lumia
        r'(lenovo)[-_ ]?([-\w]+)',  # Lenovo
        r'(jolla)',  # Jolla
        r'(oppo) ?([\w ]+) bui'  # OPPO
    ], ['vendor', 'model', ['type', 'mobile']], [
        r'(archos) (gamepad2?)',  # Archos
        r'(hp).+(touchpad(?!.+tablet)|tablet)',  # HP TouchPad
        r'(kindle)\/([\w\.]+)',  # Kindle
        r'(nook)[\w ]+build\/(\w+)',  # Nook
        r'(dell) (strea[kpr\d ]*[\dko])',  # Dell Streak
        r'(le[- ]+pan)[- ]+(\w{1,9}) bui',  # Le Pan Tablets
        r'(trinity)[- ]*(t\d{3}) bui',  # Trinity Tablets
        r'(gigaset)[- ]+(q\w{1,9}) bui',  # Gigaset Tablets
        r'(vodafone) ([\w ]+)(?:\)| bui)'  # Vodafone
    ], ['vendor', 'model', ['type', 'tablet']], [

        r'(surface duo)'  # Surface Duo
    ], ['model', ['vendor', 'Microsoft'], ['type', 'tablet']], [
        r'droid [\d\.]+; (fp\du?)(?: b|\))'  # Fairphone
    ], ['model', ['vendor', 'Fairphone'], ['type', 'mobile']], [
        r'(u304aa)'  # AT&T
    ], ['model', ['vendor', 'AT&T'], ['type', 'mobile']], [
        r'\bsie-(\w*)'  # Siemens
    ], ['model', ['vendor', 'Siemens'], ['type', 'mobile']], [
        r'\b(rct\w+) b'  # RCA Tablets
    ], ['model', ['vendor', 'RCA'], ['type', 'tablet']], [
        r'\b(venue[\d ]{2,7}) b'  # Dell Venue Tablets
    ], ['model', ['vendor', 'Dell'], ['type', 'tablet']], [
        r'\b(q(?:mv|ta)\w+) b'  # Verizon Tablet
    ], ['model', ['vendor', 'Verizon'], ['type', 'tablet']], [
        r'\b(?:barnes[& ]+noble |bn[rt])([\w\+ ]*) b'  # Barnes & Noble Tablet
    ], ['model', ['vendor', 'Barnes & Noble'], ['type', 'tablet']], [
        r'\b(tm\d{3}\w+) b'
    ], ['model', ['vendor', 'NuVision'], ['type', 'tablet']], [
        r'\b(k88) b'  # ZTE K Series Tablet
    ], ['model', ['vendor', 'ZTE'], ['type', 'tablet']], [
        r'\b(nx\d{3}j) b'  # ZTE Nubia
    ], ['model', ['vendor', 'ZTE'], ['type', 'mobile']], [
        r'\b(gen\d{3}) b.+49h'  # Swiss GEN Mobile
    ], ['model', ['vendor', 'Swiss'], ['type', 'mobile']], [
        r'\b(zur\d{3}) b'  # Swiss ZUR Tablet
    ], ['model', ['vendor', 'Swiss'], ['type', 'tablet']], [
        r'\b((zeki)?tb.*\b) b'  # Zeki Tablets
    ], ['model', ['vendor', 'Zeki'], ['type', 'tablet']], [
        r'\b([yr]\d{2}) b',
        r'\b(dragon[- ]+touch |dt)(\w{5}) b'  # Dragon Touch Tablet
    ], [['vendor', 'Dragon Touch'], 'model', ['type', 'tablet']], [
        r'\b(ns-?\w{0,9}) b'  # Insignia Tablets
    ], ['model', ['vendor', 'Insignia'], ['type', 'tablet']], [
        r'\b((nxa|next)-?\w{0,9}) b'  # NextBook Tablets
    ], ['model', ['vendor', 'NextBook'], ['type', 'tablet']], [
        r'\b(xtreme\_)?(v(1[045]|2[015]|[3469]0|7[05])) b'  # Voice Xtreme Phones
    ], [['vendor', 'Voice'], 'model', ['type', 'mobile']], [
        r'\b(lvtel\-)?(v1[12]) b'  # LvTel Phones
    ], [['vendor', 'LvTel'], 'model', ['type', 'mobile']], [
        r'\b(ph-1) '  # Essential PH-1
    ], ['model', ['vendor', 'Essential'], ['type', 'mobile']], [
        r'\b(v(100md|700na|7011|917g).*\b) b'  # Envizen Tablets
    ], ['model', ['vendor', 'Envizen'], ['type', 'tablet']], [
        r'\b(trio[-\w\. ]+) b'  # MachSpeed Tablets
    ], ['model', ['vendor', 'MachSpeed'], ['type', 'tablet']], [
        r'\btu_(1491) b'  # Rotor Tablets
    ], ['model', ['vendor', 'Rotor'], ['type', 'tablet']], [
        r'(shield[\w ]+) b'  # Nvidia Shield Tablets
    ], ['model', ['vendor', 'Nvidia'], ['type', 'tablet']], [
        r'(sprint) (\w+)'  # Sprint Phones
    ], ['vendor', 'model', ['type', 'mobile']], [
        r'(kin\.[onetw]{3})'  # Microsoft Kin
    ], [['model', r'\.', ' '], ['vendor', 'Microsoft'], ['type', 'mobile']], [
        r'droid.+; (cc6666?|et5[16]|mc[239][23]x?|vc8[03]x?)\)'  # Zebra
    ], ['model', ['vendor', 'Zebra'], ['type', 'tablet']], [
        r'droid.+; (ec30|ps20|tc[2-8]\d[kx])\)'
    ], ['model', ['vendor', 'Zebra'], ['type', 'mobile']], [

        # Consoles
        r'(ouya)',  # Ouya
        r'(nintendo) ([wids3utch]+)'  # Nintendo
    ], ['vendor', 'model', ['type', 'console']], [
        r'droid.+; (shield) bui'  # Nvidia
    ], ['model', ['vendor', 'Nvidia'], ['type', 'console']], [
        r'(playstation [345portablevi]+)'  # Playstation
    ], ['model', ['vendor', 'Sony'], ['type', 'console']], [
        r'\b(xbox(?: one)?(?!; xbox))[\); ]'  # Microsoft Xbox
    ], ['model', ['vendor', 'Microsoft'], ['type', 'console']], [

        # SmartTVs
        r'smart-tv.+(samsung)'  # Samsung
    ], ['vendor', ['type', 'smarttv']], [
        r'hbbtv.+maple;(\d+)'
    ], [['model', '^', 'SmartTV'], ['vendor', 'Samsung'], ['type', 'smarttv']], [
        r'(nux; netcast.+smarttv|lg (netcast\.tv-201\d|android tv))'  # 'LG' SmartTV
    ], [['vendor', 'LG'], ['type', 'smarttv']], [
        r'(apple) ?tv'  # Apple TV
    ], ['vendor', ['model', 'Apple' + ' TV'], ['type', 'smarttv']], [
        r'crkey'  # Google Chromecast
    ], [['model', 'Chrome' + 'cast'], ['vendor', 'Google'], ['type', 'smarttv']], [
        r'droid.+aft(\w)( bui|\))'  # Fire TV
    ], ['model', ['vendor', 'Amazon'], ['type', 'smarttv']], [
        r'\(dtv[\);].+(aquos)'  # Sharp
    ], ['model', ['vendor', 'Sharp'], ['type', 'smarttv']], [
        r'\b(roku)[\dx]*[\)\/]((?:dvp-)?[\d\.]*)',  # Roku
        r'hbbtv\/\d+\.\d+\.\d+ +\([\w ]*; *(\w[^;]*);([^;]*)'  # HbbTV devices
    ], [['vendor', trim], ['model', trim], ['type', 'smarttv']], [
        r'\b(android tv|smart[- ]?tv|opera tv|tv; rv:)\b'  # SmartTV from Unidentified Vendors
    ], [['type', 'smarttv']], [

        # Wearables
        r'((pebble))app'  # Pebble
    ], ['vendor', 'model', ['type', 'wearable']], [
        r'droid.+; (glass) \d'  # Google Glass
    ], ['model', ['vendor', 'Google'], ['type', 'wearable']], [
        r'droid.+; (wt63?0{2,3})\)'
    ], ['model', ['vendor', 'Zebra'], ['type', 'wearable']], [
        r'(quest( 2)?)'  # Oculus Quest
    ], ['model', ['vendor', 'Facebook'], ['type', 'wearable']], [

        # Embedded
        r'(tesla)(?: qtcarbrowser|\/[-\w\.]+)'  # Tesla
    ], ['vendor', ['type', 'embedded']], [

        # Mixed (Generic)
        r'droid .+?; ([^;]+?)(?: bui|\) applew).+? mobile safari'  # Android Phones from Unidentified Vendors
    ], ['model', ['type', 'mobile']], [
        r'droid .+?; ([^;]+?)(?: bui|\) applew).+?(?! mobile) safari'  # Android Tablets from Unidentified Vendors
    ], ['model', ['type', 'tablet']], [
        r'\b((tablet|tab)[;\/]|focus\/\d(?!.+mobile))'  # Unidentifiable Tablet
    ], [['type', 'tablet']], [
        r'(phone|mobile(?:[;\/]| safari)|pda(?=.+windows ce))'  # Unidentifiable Mobile
    ], [['type', 'mobile']], [
        r'(android[-\w\. ]{0,9});.+buil'  # Generic Android Device
    ], ['model', ['vendor', 'Generic']]],

    'engine': [[
        r'windows.+ edge\/([\w\.]+)'  # EdgeHTML
    ], ['version', ['name', 'Edge' + 'HTML']], [
        r'webkit\/537\.36.+chrome\/(?!27)([\w\.]+)'  # Blink
    ], ['version', ['name', 'Blink']], [
        r'(presto)\/([\w\.]+)',  # Presto
        r'(webkit|trident|netfront|netsurf|amaya|lynx|w3m|goanna)\/([\w\.]+)',  # WebKit/Trident/NetFront/NetSurf/Amaya/Lynx/w3m/Goanna
        r'ekioh(flow)\/([\w\.]+)',  # Flow
        r'(khtml|tasman|links)[\/ ]\(?([\w\.]+)',  # KHTML/Tasman/Links
        r'(icab)[\/ ]([23]\.[\d\.]+)'  # iCab
    ], ['name', 'version'], [
        r'rv\:([\w\.]{1,9})\b.+(gecko)'  # Gecko
    ], ['version', 'name']],

    'os': [[
        # Windows
        r'microsoft (windows) (vista|xp)'  # Windows (iTunes)
    ], ['name', 'version'], [
        r'(windows) nt 6\.2; (arm)',  # Windows RT
        r'(windows (?:phone(?: os)?|mobile))[\/ ]?([\d\.\w ]*)',  # Windows Phone
        r'(windows)[\/ ]?([ntce\d\. ]+\w)(?!.+xbox)'
    ], ['name', ['version', str_mapper, WINDOWS_VERSION_MAP]], [
        r'(win(?=3|9|n)|win 9x )([nt\d\.]+)'
    ], [['name', 'Windows'], ['version', str_mapper, WINDOWS_VERSION_MAP]], [

        # iOS/macOS
        r'ip[honead]{2,4}\b(?:.*os ([\w]+) like mac|; opera)',  # iOS
        r'cfnetwork\/.+darwin'
    ], [['version', '_', '.'], ['name', 'iOS']], [
        r'(mac os x) ?([\w\. ]*)',
        r'(macintosh|mac_powerpc\b)(?!.+haiku)'  # Mac OS
    ], [['name', 'Mac OS'], ['version', '_', '.']], [

        # Mobile OSes
        r'droid ([\w\.]+)\b.+(android[- ]x86)'  # Android-x86
    ], ['version', 'name'], [
        r'(android|webos|qnx|bada|rim tablet os|maemo|meego|sailfish)[-\/ ]?([\w\.]*)',  # Android/WebOS/QNX/Bada/RIM/Maemo/MeeGo/Sailfish OS
        r'(blackberry)\w*\/([\w\.]*)',  # Blackberry
        r'(tizen|kaios)[\/ ]([\w\.]+)',  # Tizen/KaiOS
        r'\((series40);'  # Series 40
    ], ['name', 'version'], [
        r'\(bb(10);'  # BlackBerry 10
    ], ['version', ['name', 'BlackBerry']], [
        r'(?:symbian ?os|symbos|s60(?=;)|series60)[-\/ ]?([\w\.]*)'  # Symbian
    ], ['version', ['name', 'Symbian']], [
        r'mozilla\/[\d\.]+ \((?:mobile|tablet|tv|mobile; [\w ]+); rv:.+ gecko\/([\w\.]+)'  # Firefox OS
    ], ['version', ['name', 'Firefox' + ' OS']], [
        r'web0s;.+rt(tv)',
        r'\b(?:hp)?wos(?:browser)?\/([\w\.]+)'  # WebOS
    ], ['version', ['name', 'webOS']], [

        # Google Chromecast
        r'crkey\/([\d\.]+)'  # Google Chromecast
    ], ['version', ['name', 'Chrome' + 'cast']], [
        r'(cros) [\w]+ ([\w\.]+\w)'  # Chromium OS
    ], [['name', 'Chromium OS'], 'version'], [

        # Console
        r'(nintendo|playstation) ([wids345portablevuch]+)',  # Nintendo/Playstation
        r'(xbox); +xbox ([^\);]+)',  # Microsoft Xbox (360, One, X, S, Series X, Series S)

        # Other
        r'\b(joli|palm)\b ?(?:os)?\/?([\w\.]*)',  # Joli/Palm
        r'(mint)[\/\(\) ]?(\w*)',  # Mint
        r'(mageia|vectorlinux)[; ]',  # Mageia/VectorLinux
        r'([kxln]?ubuntu|debian|suse|opensuse|gentoo|arch(?= linux)|slackware|fedora|mandriva|centos|pclinuxos|red ?hat|zenwalk|linpus|raspbian|plan 9|minix|risc os|contiki|deepin|manjaro|elementary os|sabayon|linspire)(?: gnu\/linux)?(?: enterprise)?(?:[- ]linux)?(?:-gnu)?[-\/ ]?(?!chrom|package)([-\w\.]*)',  # Ubuntu/Debian/SUSE/Gentoo/Arch/Slackware/Fedora/Mandriva/CentOS/PCLinuxOS/RedHat/Zenwalk/Linpus/Raspbian/Plan9/Minix/RISCOS/Contiki/Deepin/Manjaro/elementary/Sabayon/Linspire
        r'(hurd|linux) ?([\w\.]*)',  # Hurd/Linux
        r'(gnu) ?([\w\.]*)',  # GNU
        r'\b([-frentopcghs]{0,5}bsd|dragonfly)[\/ ]?(?!amd|[ix346]{1,2}86)([\w\.]*)',  # FreeBSD/NetBSD/OpenBSD/PC-BSD/GhostBSD/DragonFly
        r'(haiku) (\w+)'  # Haiku
    ], ['name', 'version'], [
        r'(sunos) ?([\w\.\d]*)'  # Solaris
    ], [['name', 'Solaris'], 'version'], [
        r'((?:open)?solaris)[-\/ ]?([\w\.]*)',  # Solaris
        r'(aix) ((\d)(?=\.|\)| )[\w\.])*',  # AIX
        r'\b(beos|os\/2|amigaos|morphos|openvms|fuchsia|hp-ux)',  # BeOS/OS2/AmigaOS/MorphOS/OpenVMS/Fuchsia/HP-UX
        r'(unix) ?([\w\.]*)'  # UNIX
    ], ['name', 'version']]
}

# compile regexes
for regexes in REGEXES.values():
    for idx in range(0, len(regexes), 2):
        regexes[idx] = [re.compile(r, re.IGNORECASE) for r in regexes[idx]]

