from bs4 import BeautifulSoup
import random
import requests

USER_AGENT_SCRAPER_BASE_URL = 'http://www.useragentstring.com/pages/useragentstring.php?name='

POPULAR_BROWSERS = ['Chrome', 'Firefox', 'Mozilla', 'Safari', 'Opera', 'Opera Mini', 'Edge', 'Internet Explorer']

def get_user_agent_strings_for_this_browser(browser):
    """
    Get the latest User-Agent strings of the given Browser
    :param browser: string of given Browser
    :return: list of User agents of the given Browser
    """

    url      = USER_AGENT_SCRAPER_BASE_URL + browser
    response = requests.get(url)
    soup     = BeautifulSoup(response.content, 'html.parser')
    uaLinks  = soup.find('div', {'id': 'liste'}).findAll('a')[:20]

    return [str(user_agent.text) for user_agent in uaLinks]


def get_user_agents():
    """
    Gather a list of some active User-Agent strings from
    http://www.useragentstring.com of some of the Popular Browsers
    :return: list of User-Agent strings
    """
    user_agents = []
    for browser in POPULAR_BROWSERS:
        user_agents.extend(get_user_agent_strings_for_this_browser(browser))

    return user_agents[3:] # Remove the first 3 Google Header texts from Chrome's user agents

proxy_user_agents = get_user_agents()

# To randomly select an User-Agent from the collected user-agent strings
random_user_agent = random.choice(proxy_user_agents)

print(len(proxy_user_agents))