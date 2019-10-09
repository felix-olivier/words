import csv
import nltk.data
import pyphen
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from operator import itemgetter

# setup
sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
pyphen.language_fallback('nl_NL_variant1')
hyphenator = pyphen.Pyphen(lang='nl_NL')



# rate
def rate_text_difficulty(article_text: str):
    """
    Bereken de moeilijkheidsgraad van de tekst
    :param article_text: Volledige tekst van het artikel, als een enkele string
    :return: object met ratings per evaluatiemethode
    """
    sentence_lengths = [len(sentence.split()) for sentence in sentence_tokenizer.tokenize(article_text.strip())]
    syllable_lengths = [len(hyphenator.inserted(token).split('-')) for token in article_text.split() if len(token) > 0]


    # if (len(sentence_lengths) == 0):
    #     print('skip div by zero')
    #     len(sentence.split())
    #     print(article_text)
    #     return 0

    avg_sentence_length = sum(sentence_lengths) / len(sentence_lengths)
    avg_syllable_length = sum(syllable_lengths) / len(syllable_lengths)

    douma = 207 - .93 * avg_sentence_length - 77 * avg_syllable_length,
    brouwer = 195 - 2 * avg_sentence_length - 67 * avg_syllable_length

    return douma[0]


# with open('grading/data/articles_test.csv') as csvfile:
# with open('grading/data/trump.csv') as csvfile:
# with open('../../Desktop/vm_query.csv') as csvfile:
with open('../../Desktop/prod_result.csv') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    results = {}
    owner_results = {}
    sorted_ids = {}
    pos_sorted_ids = {}
    row_count = 10#  sum(1 for row in reader)
    i = 0
    for row in reader:
        i += 1
        print('processing article # ' + str(i) + '/' + str(row_count))

        if (row['label'] not in results):
            results[row['label']] = []
        if (row['name'] not in owner_results):
            owner_results[row['name']] = []

        if (row['text'] is not None and len(row['text']) > 0):
            score = rate_text_difficulty(row['text'])
            results[row['label']].append(score)
            owner_results[row['name']].append(score)
            sorted_ids[row['id']] = score
            if (score > 0):
                pos_sorted_ids[row['id']] = score




##### plotting by category
fig = plt.figure(1, figsize=(20, 6), dpi=80, facecolor='w', edgecolor='k')
ax = fig.add_subplot(111)

values = []
names = []
plottables = ['Economie', 'Tech', 'Voetbal', 'Opmerkelijk', 'Koningshuis']
for category in results:
    if (True or category in plottables):
        values.append(results[category])
        names.append(category)


# bp = ax.boxplot(values)
bp = ax.boxplot(values, 0, '')
plt.xticks(range(1, len(names) +1), names)
plt.ylabel('Readability score')

fig.savefig('Readability_by_category-t.png', bbox_inches='tight')



##### plotting by owner
fig = plt.figure(2, figsize=(20, 6), dpi=80, facecolor='w', edgecolor='k')
ax = fig.add_subplot(111)

values = []
names = []
for owner in owner_results:
        values.append(owner_results[owner])
        names.append(owner)


bp = ax.boxplot(values, 0, '')
plt.xticks(range(1, len(names) +1), names)
plt.ylabel('Readability score')

fig.savefig('Readability_by_owner-t.png', bbox_inches='tight')



## Lookup outliers
print('---------------------------------')
print('Most difficult articles: ')
most_difficult = (sorted(sorted_ids.items(), key=itemgetter(1)))[:5]
for el in most_difficult:
    print(el[0] + ' --- score: ' + str(el[1]))
print('\n\n')

print('Easiest articles: ')
most_difficult = (sorted(sorted_ids.items(), key=itemgetter(1)))[-5:]
for el in most_difficult:
    print(el[0] + ' --- score: ' + str(el[1]))

print('\n\n')

print('Most difficult but positive: ')
most_difficult = (sorted(pos_sorted_ids.items(), key=itemgetter(1)))[:5]
for el in most_difficult:
    print(el[0] + ' --- score: ' + str(el[1]))
