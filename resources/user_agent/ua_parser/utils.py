
def strMapper(
    str_: str,  # String to be mapped to the value of the corresponding key of the mapping dictionary 
    map_: dict, # Mapper dictionary
    UNK = '?'   # Token used as unknown key
    ):
    """ Maps a string to the corresponding value of a dictionary """

    for key, value in map_.items():
        if key.lower() in str_.lower():
            if value == UNK : return None
            else            : return value
    
    return str_ # If you reach this point, return the input string
