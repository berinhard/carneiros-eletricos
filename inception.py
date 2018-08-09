#!/usr/bin/env python
import shlex
import subprocess
import os
import click
from decouple import config
from unipath import Path


DARKNET_DIR = config('DARKNET_DIR', cast=Path)
DARKNET_BIN = config('DARKNET_BIN', default=DARKNET_DIR.child('darknet'))
VGG_CONF = config('YOLO_CONF', default=DARKNET_DIR.child('cfg', 'vgg-conv.cfg'))
VGG_WEIGHTS = config('YOLO_WEIGHTS', default=DARKNET_DIR.child('vgg-conv.weights'))


def deep_dream(image_path, out_dir):
    command = ' '.join([
        DARKNET_BIN,
        'nightmare',
        VGG_CONF,
        VGG_WEIGHTS,
        image_path,
        '1',
        '-iters',
        '1',
        '-prefix',
        out_dir,
    ])
    print('Exec --> {}'.format(command))

    detect = subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        cwd=DARKNET_DIR,
    )
    detect.wait()

    name = image_path.name.split('.')[0]
    return out_dir.listdir("{}*".format(name))


@click.command()
@click.argument('images_dir', type=click.Path(exists=True))
@click.argument('out_dir', type=click.Path(exists=False))
def dream_on_dir(images_dir, out_dir):
    images_dir = Path(images_dir)
    out_dir = Path(out_dir)

    if not out_dir.exists():
        os.mkdir(out_dir)

    for image in images_dir.listdir():
        dream_images = deep_dream(image, out_dir)
        for d in dream_images:
            print("  New dream: {}".format(d))


if __name__ == '__main__':
    dream_on_dir()
