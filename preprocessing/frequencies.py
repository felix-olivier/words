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


def to_tokens(text: str, tokenizer):
    text = text \
        .replace('\n', ' ') \
        .replace('\r', ' ') \
        .replace('\t', ' ') \
        .replace('  ', ' ')

    filters = [
        lambda token: '<' not in token,
        lambda token: token.isalpha(),
        lambda token: len(token) > 1,
        lambda token: token[0].islower(),
        lambda token: all(c.islower() for c in token),
    ]

    return list(filter(
        lambda token: all(f(token) for f in filters),
        tokenizer.tokenize(text)
    ))


def count_occurrences(lines: list) -> dict:
    result = {}
    for line in lines:
        for token in line:
            if token not in result:
                result[token] = 0
            result[token] += 1
    return result


def export(occurrences: dict, name: str):
    pyphen.language_fallback('nl_NL_variant1')
    dic = pyphen.Pyphen(lang='nl_NL')
    with open('export/export-' + name + '.csv', 'w') as fh:
        fh.write('owner,token,stem,frequency,syllables\n')
        for token in occurrences:
            fh.write(name + ',' + token + ',' + stemmer.stem(token) + ',' + str(occurrences[token]) + ',' + str(len(dic.inserted(token).split('-'))) + '\n')


if __name__ == '__main__':
    tokenizer = TweetTokenizer()
    stemmer = DutchStemmer()

    for file in ['nieuws', 'jeugd']:
        text = load_text('input/' + file + '.csv')
        print('A')
        tokens = [to_tokens(line, tokenizer) for line in text]
        print('B')
        occurrences = count_occurrences(tokens)
        print('C')
        export(occurrences, file)


