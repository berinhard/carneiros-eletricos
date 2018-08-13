#!/usr/bin/env python
import click
import requests
import random
from unipath import Path
from urllib.parse import urlparse
from decouple import config

AZURE_SUBSCRIPTION_KEY = config('AZURE_SUBSCRIPTION_KEY')
SEARCH_URL = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"


def get_search_results(search_term):
    headers = {"Ocp-Apim-Subscription-Key": AZURE_SUBSCRIPTION_KEY}
    params = {"q": search_term, "license": "public", "imageType": "photo"}
    response = requests.get(SEARCH_URL, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    return search_results['value']


def write_image(image_url):
    parsed_url = urlparse(image_url)
    name, ext = Path(parsed_url.path).name.split('.')
    name = name[:20]

    response = requests.get(image_url)
    response.raise_for_status()

    output_image = Path('/', 'tmp', '{}.{}'.format(name, ext))
    with open(output_image, 'wb') as fd:
        fd.write(response.content)

    return output_image


@click.command()
@click.argument('search_term', type=str)
def search_random_image(search_term):
    images = get_search_results(search_term)
    random_image = random.choice(images)
    downloaded_image = write_image(random_image['contentUrl'])
    print('New image at {}'.format(downloaded_image))


if __name__ == '__main__':
    search_random_image()
