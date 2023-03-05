
from typing  import Union

def strMapper(
    str_: str,         # String to be mapped to the value of the corresponding key of the map_ dict 
    map_: dict,        # Mapper dictionary
    UNK : str  = '?'   # Token used as unknown key
    ) -> Union[str, None]:
    """ Maps a string to the corresponding value of a dictionary """

    for key, value in map_.items():

        if key.lower() in str_.lower():

            if value == UNK : return None
            else            : return value
    
    return str_ # If you reach this point, return the input string


