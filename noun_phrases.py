#!/usr/bin/env python
import click
import nltk


@click.command()
@click.argument('infile', type=click.File('r'))
@click.argument('outfile', type=click.File('w'))
def extract_noun_phrases(infile, outfile):
    contents = infile.read()

    sentences = [nltk.word_tokenize(sent) for sent in
                 nltk.sent_tokenize(contents)]
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
                outfile.write(np)
                outfile.write('\n')


if __name__ == '__main__':
    extract_noun_phrases()
