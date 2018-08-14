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
    params = {
        "q": search_term,
        "license": "public",
        "imageType": "photo",
        "maxWidth": "900",
        "maxHeight": "900",
    }
    response = requests.get(SEARCH_URL, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    return search_results['value']


def write_image(image_url, download_dir):
    parsed_url = urlparse(image_url)
    name, ext = Path(parsed_url.path).name.split('.')
    name = name[:20]

    response = requests.get(image_url)
    response.raise_for_status()

    output_image = download_dir.child('{}.{}'.format(name, ext))
    with open(output_image, 'wb') as fd:
        fd.write(response.content)

    return output_image


def search_random_image(search_term, download_dir):
    download_dir = Path(download_dir)

    images = get_search_results(search_term)
    random_image = random.choice(images)
    downloaded_image = write_image(random_image['contentUrl'], download_dir)
    print('New image at {}'.format(downloaded_image))
    return downloaded_image


@click.command()
@click.argument('search_term', type=str)
@click.option('--download_dir', default='/tmp', help='Download dir', type=click.Path(exists=True))
def search_random_image_cli(*args, **kwargs):
    search_random_image(*args, **kwargs)


if __name__ == '__main__':
    search_random_image_cli()
