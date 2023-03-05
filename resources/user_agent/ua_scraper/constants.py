
"""
List of browser names that can be scraped from https://www.useragentstring.com/pages/Browserlist/.
Retrieved from https://www.useragentstring.com/pages/Browserlist/
"""

BASE_URL = 'http://www.useragentstring.com/pages/useragentstring.php?name={name}'


DEFAULT_BROWSERS   = ['chrome', 'firefox', 'safari', 'edge']
AVAILABLE_BROWSERS = {
    'abrowse',          'acoo browser', 'america online browser', 'arora',      'amigavoyager',       'aol',
    'avant browser',    'beonex',       'bonecho',          'browzar',          'camino',             'charon',
    'cheshire',         'chimera',      'chrome',           'chromeplus',       'classilla',          'cometbird',
    'comodo_dragon',    'conkeror',     'crazy browser',    'cyberdog',         'deepnet explorer',   'deskbrowse',
    'dillo',            'dooble',       'edge',             'element browser',  'elinks',             'enigmafox',
    'epiphany',         'escape',       'firebird',         'firefox',          'fireweb navigator',  'safari',
    'flock',            'fluid',        'galaxy',           'galeon',           'granparadiso',       'greenbrowser',
    'hana',             'hotjava',      'ibm webexplorer',  'ibrowse',          'icab',               'iceape',
    'iceCat',           'iceweasel',    'inet browser',     'internet explorer','irider',             'iron',
    'k-meleon',         'k-ninja',      'kapiko',           'kazehakase',       'kkman',              'kmlite',
    'konqueror',        'leechcraft',   'links',            'lobo',             'lolifox',            'lorentz',
    'lunascape',        'lynx',         'madfox',           'maxthon',          'midori',             'minefield',
    'mozilla',          'myibrow',      'myie2',            'namoroka',         'navscape',           'ncsa_mosaic',
    'netnewswire',      'netpositive',  'netscape',         'netsurf',          'omniweb',            'opera',
    'orca',             'oregano',      'osb-browser',      'palemoon',         'phoenix',            'pogo',
    'prism',            'qtweb internet browser',           'rekonq',           'retawq',             'rockmelt',
    'seamonkey',        'shiira',       'shiretoko',        'sleipnir',         'slimbrowser',        'stainless',
    'sundance',         'sunrise',      'surf',             'sylera',           'tencent traveler',   'tenfourfox',
    'theworld browser', 'uzbl',         'vimprobable',      'vonkeror',         'w3m',                'weltweitimnetzbrowser',
    'worldwideweb',     'wyzo'}