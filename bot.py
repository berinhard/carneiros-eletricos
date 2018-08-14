#!/usr/bin/env python
from time import sleep
import click
import os
from unipath import Path

from image_search import search_random_image
from inception import deep_dream, NightmareConfig


FIRST_PAGE = [
    'merry',
    'little surge',
    'electricity',
    'automatic alarm',
    'the mood',
    'bed',
    'prior notice',
    'the bed',
    'multicolored pajamas',
    'bed',
    'wife',
    'hand',
    'voice',
    'bitter sharpness',
    'bent',
    'the surge',
    'the whole point',
    'the threshold barring',
    'consciousness',
    'the world',
    'setting',
    'bare',
    'pate shoulder',
    'crude',
    'cop',
    'hand',
    'a cop',
    'wife',
    'a murderer',
    'life',
    'irritability',
    'outright hostility',
    'those poor andys',
    'any hesitation',
    'the bounty',
    'money',
    'home',
    'attention',
    'strode',
    'the console',
    'mood',
    'organ',
    'a real sheep',
    'that fake',
    'upstairs',
    'A mere electric animal',
    'way',
    'console',
    'a thalamic suppressant',
    'mood',
    'rage',
    'a thalamic stimulant',
    'the argument',
    'watching',
    'venom',
    'the maximum',
    'a fight',
    'every argument',
    'nothing',
    'the console',
    'own mood',
    'organ',
    'threat',
    'schedule',
    'today',
    'the schedule',
    'a businesslike professional attitude',
    'schedule',
    'wife',
    'suit',
]


@click.command()
@click.argument('out_dir', type=click.Path(exists=False))
def read_look_dream(out_dir):
    out_dir = Path(out_dir)
    download_dir = out_dir.child('download')

    if not out_dir.exists():
        os.mkdir(out_dir)

    if not download_dir.exists():
        os.mkdir(download_dir)

    for i, text in enumerate(FIRST_PAGE):
        print('Reading "{}"...'.format(text))
        image = search_random_image(text, download_dir)

        print('Dreaming "{}"...'.format(text))
        dirname = '000{} {}'.format(i, text).replace(' ', '_')
        config = NightmareConfig(out_dir.child(dirname))
        os.mkdir(config.out_dir)
        config.force_all_random()
        deep_dream(image, config)

        for d in config.list_output_for_image(image):
            print("  New dream: {}".format(d))

        sleep(10)
        print()


if __name__ == '__main__':
    read_look_dream()
