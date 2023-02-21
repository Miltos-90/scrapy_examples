"""
Random User-Agent
Copyright: 2022 Ekin Karadeniz (github.com/iamdual)
License: Apache License 2.0
"""
import random


def contains(t, val):
    if type(t) is str and t == val:
        return True
    if (type(t) is tuple or type(t) is list) and val in t:
        return True

    return False


def contains_multiple(t, arr):
    for val in arr:
        if contains(t, val):
            return True

    return False


def choice(t):
    if not t:
        return None
    if type(t) is str:
        return t
    if type(t) is tuple or type(t) is list:
        return random.choice(t)

    return False



def version(version_dict, strip_zero=False):
    v_str = str(version_dict['major'])

    if 'minor' in version_dict and (
            strip_zero is False or
            (strip_zero is True and version_dict['minor'] > 0)):
        v_str += '.' + str(version_dict['minor'])

    return v_str


def major_version(version_dict):
    return str(version_dict['major']).split('.', 1)[0]

