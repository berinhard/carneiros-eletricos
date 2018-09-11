#!/usr/bin/env python
import click
import csv
import os
from functools import partial
from time import sleep
from tqdm import tqdm
from unipath import Path

from src.inception import NightmareConfig, deep_dream



@click.command()
@click.argument('csv_file', type=click.File('r'))
@click.argument('out_dir', type=click.Path(exists=False))
def dream_on_csv(csv_file, out_dir):
    out_dir = Path(out_dir)
    if not out_dir.exists():
        os.mkdir(out_dir)

    config = NightmareConfig(out_dir=out_dir)

    out_csv_rows = []
    fieldnames = ['reader', 'position', 'search', 'image_file']

    reader = csv.DictReader(csv_file, fieldnames)
    for row in reader:
        config.force_all_random()
        image = Path(row['image_file'])
        deep_dream(image, config)

        outfile = ''
        outfiles = config.list_output_for_image(image)
        if outfiles:
            outfile = outfiles[0]

        out_row = row.copy()
        out_row['dream_file'] = outfile
        out_row['parameters'] = ' '.join([str(p) for p in config.parameters])
        out_csv_rows.append(out_row)

    output_fieldnames = fieldnames + ['dream_file', 'parameters']
    with open(out_dir.child('results.csv'), 'w') as fd:
        writer = csv.DictWriter(fd, output_fieldnames)
        writer.writeheader()
        writer.writerows(out_csv_rows)


if __name__ == '__main__':
    dream_on_csv()
