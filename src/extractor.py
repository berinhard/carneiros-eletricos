#!/usr/bin/env python
import click
import nltk

def noun_phrases(text, *args, **kwargs):
    sentences = (nltk.word_tokenize(sent) for sent in
                 nltk.sent_tokenize(text))

    tagged_sentences = nltk.pos_tag_sents(sentences)


    # chunking baseado em https://www.nltk.org/book/ch07.html
    grammar = "NP: {<DT>?<JJ.*>*<NN.*>*<JJ.*>*}"

    cp = nltk.RegexpParser(grammar)

    NPs = [] # Sintagmas nominais como objetos Tree
    flat_noun_phrases = [] # Strings com os sintagmas nominais
    for sentence_tree in cp.parse_sents(tagged_sentences):
        for subtree in sentence_tree.subtrees():
            if subtree.label() == "NP":
                NPs.append(subtree)
                np = ' '.join(w[0] for w in subtree.leaves())
                flat_noun_phrases.append(np)
                yield np

def all_words(text, *args, **kwargs):
    tokenizer = nltk.RegexpTokenizer(r'[\w\d\'-]+')
    return tokenizer.tokenize(text)

def ngram(text, *args, **kwargs):
    size = kwargs.get('ngram_size', 2)
    words = all_words(text)
    result = nltk.ngrams(words, size)
    for result in result:
        yield ' '.join(result)


def extract_ngrams(text, *args, **kwargs):
    min_size = kwargs.get('min_ngram_size', 1)
    size = kwargs.get('ngram_size', 2)
    for n in range(min_size, size + 1):
        ngram_result = ngram(text, ngram_size=n)
        for result in ngram_result:
            yield result


available_functions = {
    'noun_phrases': noun_phrases,
    'all_words': all_words,
    'ngram': ngram,
    'ngrams': extract_ngrams,
}


@click.command()
@click.argument('infile', type=click.File('r'))
@click.argument('outfile', type=click.File('w'))
@click.option(
    '--function', default='noun_phrases',
    type=click.Choice(list(available_functions.keys()))
)
@click.option('--ngram-size', type=int, default=2)
@click.option('--min-ngram-size', type=int, default=1)
def extract_words(infile, outfile, function, *args, **kwargs):
    contents = infile.read()
    f_to_call = available_functions.get(function)
    words = f_to_call(contents, *args, **kwargs)
    for word in words:
        outfile.write(word)
        outfile.write('\n')

if __name__ == '__main__':
    extract_words()
