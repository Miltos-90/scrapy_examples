from .parser import Parser

""" Compile all regexes when imported """
from .constants import BROWSER, CPU, DEVICE, ENGINE, OS
import re

for list_ in [BROWSER, CPU, DEVICE, ENGINE, OS]:
    for dict_ in list_: 
        dict_['regex'] = re.compile(dict_['regex'], re.IGNORECASE)