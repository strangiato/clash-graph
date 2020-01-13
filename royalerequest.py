import os
import requests
import json

def getBaseURL():
    return "https://api.royaleapi.com"

def getHeaders():

    api_key = os.getenv('CLASH_API')

    headers = {
        'auth': api_key
        }

    return headers

def getClan(base_url, headers, tag):
    print("Get Clan: {}".format(tag))
    request_url = '{base_url}/clan/{tag}'.format(base_url = base_url, tag = tag)
    return __getData(request_url, headers)

def getCards(base_url, headers):
    print("Get Cards")
    request_url = '{base_url}/constant/cards'.format(base_url = base_url)
    return __getData(request_url, headers)

def getPlayer(base_url, headers, tag):
    print("Get Player: {}".format(tag))
    request_url = '{base_url}/player/{tag}'.format(base_url = base_url, tag = tag)
    return __getData(request_url, headers)

def getBattles(base_url, headers, tag):
    print("Get Player Battles: {}".format(tag))
    request_url = '{base_url}/player/{tag}/battles'.format(base_url = base_url, tag = tag)
    return __getData(request_url, headers)

def getWar(base_url, headers, tag):
    print("Get Clan Current War: {}".format(tag))
    request_url = '{base_url}/clan/{tag}/war'.format(base_url = base_url, tag = tag)
    return __getData(request_url, headers)

def __getData(url, headers):
    response = requests.request("GET", url, headers=headers)
    return response.json()

if __name__ == "__main__":

    base_url = getBaseURL()
    headers = getHeaders()
    print(headers)
    clan = getClan(base_url, headers, "VV80RJY")
    print(clan["tag"])

    player = getPlayer(base_url, headers, "80VUU9PLP")
    print(player["tag"])

    cards = getCards(base_url, headers)
    