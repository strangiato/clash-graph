import requests
import json

api_key = ""

base_url = "https://api.royaleapi.com"

headers = {
    'auth': api_key
    }

def getClan(base_url, headers, tag):
    request_url = '{base_url}/clan/{tag}'.format(base_url = base_url, tag = tag)
    return __getData(request_url, headers)

def getPlayer(base_url, headers, tag):
    request_url = '{base_url}/player/{tag}'.format(base_url = base_url, tag = tag)
    return __getData(request_url, headers)

def getBattles(base_url, headers, tag):
    request_url = '{base_url}/player/{tag}/battles'.format(base_url = base_url, tag = tag)
    return __getData(request_url, headers)

def __getData(url, headers):
    response = requests.request("GET", url, headers=headers)
    return response.json()

if __name__ == "__main__":

    clan = getClan(base_url, headers, "VV80RJY")

    print(clan["tag"])

    player = getPlayer(base_url, headers, "80VUU9PLP")

    print(player)