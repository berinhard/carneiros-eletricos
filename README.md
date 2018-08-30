## App setup

```bash
git clone git@github.com:berinhard/carneiros-eletricos.git
mkvirtualenv carneiros-eletricos -p /usr/bin/python3.6.5
cd caneiros-eletricos
cp env.example .env  # you'll have to set
vi .env  # you'll have to set at least the DARKNET_DIR variable to your path
pip install -r requirements.txt
```

## Extractor module

The `extractor.py` module is a CLI to generate a text file with a list of words depending on the chosen function.

Examples:
`src/extractor.py chapter_1.txt out.txt --function=ngrams --ngram-size=5 --min-ngram-size=3` will create a `out.txt` file with all ngrams from `min-ngram-size` to `ngram-size` separate by `\n`.

`src/extractor.py chapter_1.txt out.txt --function=ngram --ngram-size=5` will create a `out.txt` file with all ngrams with `ngram-size` separate by `\n`.

`src/extractor.py chapter_1.txt out.txt --function=all-words` `src/extractors.py chapter_1.txt out.txt --function=ngram --ngram-size=5` will create a `out.txt` file with all words separate by `\n`.

`src/extractor.py chapter_1.txt out.txt --function=noun-phrases` will create a `out.txt` file with all noun phrases separate by `\n`.


## Inception module

The `inception.py` module is a CLI to generate random Darknet's nightmares for images in a directory. Here's an example on how to run it:

```bash
$ ./inception ~/Desktop/images-dir/ ~/Desktop/inception-out-dir/
```


Full help:

```bash
$ ./inception.py --help
Usage: inception.py [OPTIONS] IMAGES_DIR OUT_DIR

Options:
  --help  Show this message and exit.
```


## Extracting NounPhrases

The `noun_phrases.py` script extracts noun phrases from the text. Just download the necessary nltk data:


```
nltk.download(['punkt', 'averaged_perceptron_tagger'])
```

Make sure the text is in the `data` directory and run:

```
$ ./noun_phrases.py <infile> <outfile>
```
