""" Implementation of an adapter class that modifies the user agents' parser's values (see ua_parser)
    for compatibility with the user agent generator(s).
"""

from definitions import UNKNOWN_NAME, PARSER_TYPE
from typing      import Dict, Tuple
from utils       import readFile
from ua_parser   import Parser


class Adapter():
    """ Adapter for a subset of the attribute values returned by the parser """

    def __init__(self):

        self.Parser   = Parser() # Parses an agent string (see ./ua_parser)

        # Dictionary that maps from returned parser value (key), to the value indicated here
        self.aliases: Dict[PARSER_TYPE, Dict[str, str]] = readFile('./data/parser_adapter.json')

        self.aliases.update({"device": readFile('./data/operating_systems.json')})

        return

    def get(self, 
        userAgent : str,                     # Agent from which the attribute is needdd
        attribute : Tuple[PARSER_TYPE, str], # Attribute whose value will be returned.
        ) -> str:
        """ Get an (adapted) attribute of the user agent string. """

        attr = self._getOriginal(userAgent, attribute)
        return self._modify(attribute, attr)

    
    def _getOriginal(self, 
        userAgent : str,                     # Agent from which the attribute is needdd
        attribute : Tuple[PARSER_TYPE, str]  # Attribute whose value will be returned.
        ) -> str:
        """ Get the original attribute of the user agent string from the parser"""

        if attribute == ('device', 'type'):

            # Device type will be inferred from OS name.
            osName = self.get(userAgent, attribute = ('os', 'name'))
            attr   = self.aliases["device"].get(osName, UNKNOWN_NAME)
            
        else: # Get any other attributes from the parser directly
            attr = self.Parser.get(userAgent, attribute).lower()

        return attr


    def _modify(self, 
        attribute : Tuple[PARSER_TYPE, str],  # Attribute whose value will be adapted.
        value     : str                       # Corresponding value returned by the parser
        ) -> str:
        """ Adapts the original attribute's value that was returned from the parser """

        parserName = attribute[0]                     # Get name of the parser to be used
        aliasDict  = self.aliases.get(parserName, {}) # Get the corresponding modification dictionary (if it exists)

        if bool(aliasDict):
            # Grab the property's value if it exists in the modification dict
            newValue = aliasDict.get(value)
            if newValue:
                value = newValue # Set new if exists
                

        return value

