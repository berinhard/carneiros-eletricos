#!/usr/bin/env python
import click
import os
import random
import shlex
import subprocess
from decouple import config
from unipath import Path


DARKNET_DIR = config('DARKNET_DIR', cast=Path)
DARKNET_BIN = config('DARKNET_BIN', default=DARKNET_DIR.child('darknet'))
VGG_CONF = config('YOLO_CONF', default=DARKNET_DIR.child('cfg', 'vgg-conv.cfg'))
VGG_WEIGHTS = config('YOLO_WEIGHTS', default=DARKNET_DIR.child('vgg-conv.weights'))


class NightmareConfig():
    """
    From https://pjreddie.com/darknet/nightmare/
    -rounds n: change the number of rounds (default 1). More rounds means more images generated and usually more change to the original image.
    -iters n: change the number of iterations per round (default 10). More iterations means more change to the image per round.
    -range n: change the range of possible layers (default 1). If set to one, only the given layer is chosen at every iteration. Otherwise, a layer is chosen randomly within than range (e.g. 10 -range 3 will choose between layers 9-11).
    -octaves n: change the number of possible scales (default 4). At one octave, only the full size image is examined. Each additional octave adds a smaller version of the image (3/4 the size of the previous octave).
    -rate x: change the learning rate for the image (default .05). Higher means more change to the image per iteration but also some instability and imprecision.
    -thresh x: change the threshold for features to be magnified (default 1.0). Only features over x standard deviations away from the mean are magnified in the target layer. A higher threshold means fewer features are magnified.
    -zoom x: change the zoom applied to the image after each round (default 1.0). You can optionally add a zoom in (x < 1) or zoom out (x > 1) to be applied to the image after each round.
    -rotate x: change the rotation applied after each round (default 0.0). Optional rotation after each round.
    """

    def __init__(self, out_dir, *args, **kwargs):
        self.out_dir = out_dir
        self.layers = kwargs.get('layers', 1)
        self.rounds = kwargs.get('rounds', 1)
        self.iters = kwargs.get('iters', 1)
        self.range = kwargs.get('range', 1)
        self.octaves = kwargs.get('octaves', 4)
        self.rate = kwargs.get('rate', 0.05)
        self.thresh = kwargs.get('thresh', 1)
        self.zoom = kwargs.get('zomm', 1)
        self.rotate = kwargs.get('rotate', 0)

    def cmd_str(self, image_path):
        args = [
            DARKNET_BIN,
            'nightmare',
            VGG_CONF,
            VGG_WEIGHTS,
            image_path,
            self.layers,
            '-rounds', self.rounds,
            '-iters', self.iters,
            '-range', self.range,
            '-octaves', self.octaves,
            '-rate', self.rate,
            '-thresh', self.thresh,
            '-zoom', self.zoom,
            '-rotate', self.rotate,
            '-prefix', self.out_dir
        ]
        return ' '.join([str(a) for a in args])

    def list_output_for_image(self, image_path):
        name = image_path.name.split('.')[0]
        return self.out_dir.listdir("{}*".format(name))

    def random_layers(self, choice_range=None):
        choice_range = choice_range or range(1, 20)
        self.layers = random.choice(choice_range)

    def random_rounds(self, choice_range=None):
        choice_range = choice_range or range(1, 30)
        self.rounds = random.choice(choice_range)

    def random_iters(self, choice_range=None):
        choice_range = choice_range or range(1, 20)
        self.iters = random.choice(choice_range)

    def random_range(self, choice_range=None):
        choice_range = choice_range or range(1, self.layers)
        self.range = random.choice(choice_range)

    def random_octaves(self, choice_range=None):
        choice_range = choice_range or range(1, 20)
        self.octaves = random.choice(choice_range)

    def random_zoom(self, choice_range=None):
        choice_range = choice_range or range(-1, 1)
        self.zomm = random.choice(choice_range)

    def random_rate(self):
        self.rate = random.random()

    def force_all_random(self):
        self.random_layers()
        self.random_rounds()
        self.random_iters()
        self.random_range()
        self.random_octaves()
        self.random_rate()
        self.random_zoom()


def deep_dream(image_path, config):
    command = config.cmd_str(image_path)
    print('Exec --> {}'.format(command))

    detect = subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        cwd=DARKNET_DIR,
    )
    detect.wait()


@click.command()
@click.argument('images_dir', type=click.Path(exists=True))
@click.argument('out_dir', type=click.Path(exists=False))
def dream_on_dir(images_dir, out_dir):
    images_dir = Path(images_dir)
    out_dir = Path(out_dir)

    if not out_dir.exists():
        os.mkdir(out_dir)

    for image in images_dir.listdir():
        config = NightmareConfig(out_dir=out_dir)
        config.force_all_random()
        deep_dream(image, config)
        for d in config.list_output_for_image(image):
            print("  New dream: {}".format(d))


if __name__ == '__main__':
    dream_on_dir()
