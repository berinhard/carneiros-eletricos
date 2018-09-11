#!/usr/bin/env python
import click
import csv
import os
from functools import partial
from time import sleep
from tqdm import tqdm
from unipath import Path

from src.image_search import search_random_image
from src.extractor import all_words, ngram, noun_phrases


trigram = partial(ngram, ngram_size=3)
trigram.__name__ = 'trigram'
PWD = Path(__file__).parent
READERS_FUNCTIONS = [
    all_words,
    trigram,
    noun_phrases,
]


def read(reader_func, content, out_dir):
    reader_name = reader_func.__name__
    reader_out_dir = out_dir.child(reader_name)

    if not reader_out_dir.exists():
        os.mkdir(reader_out_dir)

    texts = list(reader_func(content))
    print(f'Reading for {reader_name}')
    print(f'Num of searchs: {len(texts)}')

    with open(reader_out_dir.child('results.csv'), 'w') as fd:
        fieldnames = ['reader', 'position', 'search', 'image_file']
        csv_writer = csv.DictWriter(fd, fieldnames)
        csv_writer.writeheader()

        for i, text in tqdm(enumerate(texts[:100])):
            row = {'reader': reader_name, 'position': i, 'search': text}
            image_name = f'{i}_{text}'
            dir_content = reader_out_dir.listdir(f'{image_name}.*')

            try:
                if not dir_content:
                    image = search_random_image(text, reader_out_dir, image_name)
                else:
                    image = dir_content[0]
            except IndexError as e:
                image = ''

            row['image_file'] = image
            csv_writer.writerow(row)


@click.command()
@click.argument('chapter', type=int)
@click.argument('out_dir', type=click.Path(exists=False))
def read_and_search(chapter, out_dir):
    chapter_file = PWD.child('data').child(f'chapter_{chapter}.txt')
    if not chapter_file.exists():
        print(f'File "{chapter_file}" for chapter {chapter} does not exist.')
        return

    out_dir = Path(out_dir)
    if not out_dir.exists():
        os.mkdir(out_dir)

    with open(chapter_file, 'r') as fd:
        content = fd.read()

    for reader_func in READERS_FUNCTIONS:
        read(reader_func, content, out_dir)
        print()


if __name__ == '__main__':
    read_and_search()
