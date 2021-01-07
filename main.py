import requests
from urllib.parse import urlparse
from dotenv import load_dotenv
import os
import argparse


def get_shorten_link(url, token, long_link):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
    }
    data = {"long_url": long_link, "domain": 'bit.ly'}
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()['link']


def get_count_clicks(url, token, bitlink):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        "unit": "day",
        "units": "-1"
    }
    response = requests.get(url.format(bitlink), headers=headers)
    response.raise_for_status()
    return response.json()['total_clicks']


def get_parsed_url(url):
    parse_link_result = urlparse(url)
    link = f"{parse_link_result.netloc}{parse_link_result.path}"
    return link


def is_short_link(url, token, user_link):
    headers = {
        'Authorization': token
    }
    response = requests.get(url.format(user_link), headers=headers)
    return response.ok


def parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument('long_url', help='long link')
    args = parser.parse_args()
    long_url = args.long_url
    return long_url

if __name__ == '__main__':
    load_dotenv()
    shorten_long_url = 'https://api-ssl.bitly.com/v4/shorten'
    summary_clicks_url = 'https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary'
    info_link_url = 'https://api-ssl.bitly.com/v4/bitlinks/{}'
    bitly_token = os.getenv('BITLY_TOKEN')
    long_link = parse_command_line()
    parsed_url = get_parsed_url(long_link)
    long_or_short_link = is_short_link(info_link_url, bitly_token, parsed_url)
    try:
        if long_or_short_link:
            count_clicks_bitlink = get_count_clicks(summary_clicks_url, bitly_token, parsed_url)
            print('Число кликов по ссылке -', count_clicks_bitlink)
        else:
            bitlink = get_shorten_link(shorten_long_url, bitly_token, long_link)
            print('Ваша короткая ссылка -', bitlink)
    except requests.exceptions.HTTPError:
        print('Ошибка! Перезагрузите скрипт')
