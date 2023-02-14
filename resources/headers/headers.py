""" Generates proper headers given a user agent and referrer. Based on the idea of [1], which 
    generates headers using an HTTP Request & Response Service [2]. 
    
    User agent list from: WhatIsMyBrowser.com - User Agent Database
        This user agent database dump is provided by [3]] on Monday, February 13, 2023.
        See the following URL for a description, instructions and legal information.
    
    Referrer list with 1000 websites with the highest traffic. 
        To be used as referers for the headers.
        Modified from [4]

    Source: 
    [1] https://www.scrapehero.com/how-to-fake-and-rotate-user-agents-using-python-3/
    [2] https://httpbin.org
    [3] https://developers.whatismybrowser.com/useragents/database/
    [4] https://gist.github.com/bejaneps/ba8d8eed85b0c289a05c750b3d825f61
"""

import random
import json

UA_FILE = './user_agent_database.txt' # User agent list
R_FILE  = './referer_database.txt'    # Referer list
O_FILE  = './header_database.txt'     # Output file


def readtxt(file: str):
    """ Generic .txt file reader """

    with open(file, mode = 'r', encoding = 'utf-8') as f:
        data = f.read().splitlines()
    return data


def makeHeaders(userAgent: str, referer: str) -> dict:
    """ Header generator """

    headers = {
        'Referer'          : referer,
        'User-Agent'       : userAgent,
        'DNT'              : '1',
        'Accept'           : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection'       : 'keep-alive',
        'Accept-Language'  : 'en-US,en;q=0.5',
        'Upgrade-Insecure-Requests' : '1',
        'Accept-Encoding'  : "gzip, deflate, br"
        }
    
    return headers


if __name__ == "__main__":

    userAgentList = readtxt(UA_FILE)
    refererList   = readtxt(R_FILE)
    headerList    = []    

    for i in range(1000):
        
        headers = makeHeaders(
            userAgent = random.choice(userAgentList), 
            referer   = random.choice(refererList)
            )
        headerList.append(headers)
        

    with open(O_FILE, mode = 'w', encoding = 'utf-8') as f:
        json.dump(headerList, f, indent = 4)
