import os
import requests
import json
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

file_handler = logging.FileHandler('logs/royalerequest.log')
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def get_base_url():
    return "https://api.royaleapi.com"


def get_headers():

    API_KEY = os.getenv('CLASH_API')

    HEADERS = {
        'auth': API_KEY
    }

    return HEADERS


def get_clan(base_url, headers, tag):
    logger.info("Get Clan: {}".format(tag))
    request_url = '{base_url}/clan/{tag}'.format(base_url=base_url, tag=tag)

    return __get_data(request_url, headers)


def get_cards(base_url, headers):
    logger.info("Get Cards")
    request_url = '{base_url}/constant/cards'.format(base_url=base_url)

    return __get_data(request_url, headers)


def get_player(base_url, headers, tag):
    logger.info("Get Player: {}".format(tag))
    request_url = '{base_url}/player/{tag}'.format(base_url=base_url, tag=tag)

    return __get_data(request_url, headers)


def get_battles(base_url, headers, tag):
    logger.info("Get Player Battles: {}".format(tag))
    request_url = '{base_url}/player/{tag}/battles'.format(
        base_url=base_url, tag=tag)

    return __get_data(request_url, headers)


def get_war(base_url, headers, tag):
    logger.info("Get Clan Current War: {}".format(tag))
    request_url = '{base_url}/clan/{tag}/war'.format(
        base_url=base_url, tag=tag)

    return __get_data(request_url, headers)


def get_warlog(base_url, headers, tag):
    logger.info("Get Clan Warlog: {}".format(tag))
    request_url = '{base_url}/clan/{tag}/warlog'.format(
        base_url=base_url, tag=tag)

    return __get_data(request_url, headers)


def __get_data(url, headers):
    response = requests.request("GET", url, headers=headers)

    return response.json()


if __name__ == "__main__":

    base_url = get_base_url()
    headers = get_headers()
    print(headers)
    clan = get_clan(base_url, headers, "VV80RJY")
    print(clan["tag"])

    player = get_player(base_url, headers, "80VUU9PLP")
    print(player["tag"])

    cards = get_cards(base_url, headers)
