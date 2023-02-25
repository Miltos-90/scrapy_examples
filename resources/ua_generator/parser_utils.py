import re

UNKNOWN = '?'
EMPTY = ''



def rgx_mapper(ua, arrays):
    if not ua:
        return None

    i = 0
    matches = False
    # loop through all regexes maps
    while i < len(arrays) and not matches:
        regex = arrays[i]  # even sequence (0,2,4,..)
        props = arrays[i + 1]  # odd sequence (1,3,5,..)
        j = k = 0

        # try matching uastring with regexes
        while j < len(regex) and not matches:
            matches = regex[j].search(ua)
            j += 1
            if matches:
                for p in range(len(props)):
                    k += 1
                    try:
                        match = matches.group(k)
                    except IndexError as _:
                        match = None

                    q = props[p]
                    # check if given property is actually array
                    if isinstance(q, list):
                        if len(q) == 2:
                            if callable(q[1]):
                                # assign modified match
                                yield q[0], q[1](match)
                            else:
                                # assign given value, ignore regex match
                                yield q[0], q[1]
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
        i += 2




def majorize(version):
    if version is not None:
        return re.sub(r'[^\d\.]', EMPTY, version).split('.')[0]
    return None



def str_mapper(string, mapping):
    for key, value in mapping.items():
        # check if current value is array
        if isinstance(value, list):
            for item in value:
                if has(item, string):
                    return None if key == UNKNOWN else key
        elif has(value, string):
            return None if key == UNKNOWN else key
    return string



def has(str1, str2):
    if isinstance(str1, str):
        return lowerize(str1) in lowerize(str2)
    return False



def lowerize(string):
    return string.lower()



def trim(string):
    return re.sub(r'\s\s*$', EMPTY, re.sub(r'^\s\s*', EMPTY, string))




