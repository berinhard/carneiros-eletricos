## App setup

```bash
git clone git@github.com:berinhard/carneiros-eletricos.git
mkvirtualenv carneiros-eletricos -p /usr/bin/python3.6.5
cd caneiros-eletricos
cp env.example .env  # you'll have to set
vi .env  # you'll have to set at least the DARKNET_DIR variable to your path
pip install -r requirements.txt
```

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
