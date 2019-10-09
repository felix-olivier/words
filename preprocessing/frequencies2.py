from nltk.stem.snowball import DutchStemmer
from nltk.tokenize import TweetTokenizer
import pyphen


def load_text(file: str):
    with open(file) as fp:
        lines = []
        line = fp.readline()
        while line:
            lines.append(line)
            line = fp.readline()
    return lines




def export(tokens: list, name: str):
    pyphen.language_fallback('nl_NL_variant1')
    dic = pyphen.Pyphen(lang='nl_NL')
    with open('export/export-unknown.csv', 'w') as fh:
        fh.write('owner,token,stem,frequency,syllables\n')
        for token in tokens:
            fh.write(name + ',' + token.strip() + ',' + stemmer.stem(token.strip()) + ',0,' + str(len(dic.inserted(token).split('-'))) + '\n')


if __name__ == '__main__':
    tokenizer = TweetTokenizer()
    stemmer = DutchStemmer()

    tokens = load_text('input/extreem-zeldzame-woorden.csv')
    export(tokens, 'none')


