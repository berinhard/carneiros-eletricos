#!/usr/bin/env python
from inception import NightmareConfig, deep_dream

import click
import os
from unipath import Path


@click.command()
@click.argument('image_path', type=click.Path(exists=True))
@click.argument('test_parameter', type=str)
@click.argument('out_dir', type=click.Path(exists=False))
def test_parameters(image_path, test_parameter, out_dir):
    image_path = Path(image_path)
    out_dir = Path(out_dir)

    if not out_dir.exists():
        os.mkdir(out_dir)

    config = NightmareConfig(out_dir=out_dir)
    if test_parameter == 'layers':
        for i in range(1, 21):
            config.layers = i
            deep_dream(image_path, config)
    elif test_parameter == 'rounds':
        for i in range(1, 21):
            config.rounds = i
            deep_dream(image_path, config)
    elif test_parameter == 'iters':
        for i in range(1, 15):
            config.iters = i
            deep_dream(image_path, config)
    elif test_parameter == 'range':
        for i in range(1, 11):
            dirname = '000{}'.format(i)
            path = out_dir.child(dirname)
            os.mkdir(path)
            config = NightmareConfig(path)
            config.range = i
            deep_dream(image_path, config)
    elif test_parameter == 'octaves':
        for i in range(1, 21):
            dirname = '000{}'.format(i)
            path = out_dir.child(dirname)
            os.mkdir(path)
            config = NightmareConfig(path)
            config.octaves = i
            deep_dream(image_path, config)
    elif test_parameter == 'rate':
        for i in range(1, 11):
            dirname = '000{}'.format(i)
            path = out_dir.child(dirname)
            os.mkdir(path)
            config = NightmareConfig(path)
            config.rate = i / 10
            deep_dream(image_path, config)
    else:
        print('Parameter "{}" is invalid.'.format(test_parameter))
        return

if __name__ == '__main__':
    test_parameters()
