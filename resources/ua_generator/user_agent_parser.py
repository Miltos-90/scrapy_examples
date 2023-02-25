from parser_utils import trim, majorize, rgx_mapper
from parser_regex import REGEXES

UA_MAX_LENGTH = 255 # Maximum user agent string length

class UAParser:
    """Python implementation of User Agent parser. Fork UAParser.js"""

    def __init__(self, ua):
        self._ua = trim(ua)[0:UA_MAX_LENGTH] if ua and len(ua) > UA_MAX_LENGTH else ua

    @classmethod
    def parse(cls, ua):
        self = cls(ua)
        return {
            'ua': self.ua,
            'browser': self.browser,
            'cpu': self.cpu,
            'device': self.device,
            'engine': self.engine,
            'os': self.os
        }

    @property
    def browser(self):
        _browser = {'name': None, 'version': None, 'major_version': None}
        for key, value in rgx_mapper(self._ua, REGEXES['browser']):
            _browser[key] = value
        _browser['major_version'] = majorize(_browser['version'])
        return _browser

    @property
    def cpu(self):
        _cpu = {'architecture': None}
        for key, value in rgx_mapper(self._ua, REGEXES['cpu']):
            _cpu[key] = value
        return _cpu

    @property
    def device(self):
        _device = {'vendor': None, 'model': None, 'type': None}
        for key, value in rgx_mapper(self._ua, REGEXES['device']):
            _device[key] = value
        return _device

    @property
    def engine(self):
        _engine = {'name': None, 'version': None}
        for key, value in rgx_mapper(self._ua, REGEXES['engine']):
            _engine[key] = value
        return _engine

    @property
    def os(self):
        _os = {'name': None, 'version': None}
        for key, value in rgx_mapper(self._ua, REGEXES['os']):
            _os[key] = value
        return _os

    @property
    def ua(self):
        return self._ua