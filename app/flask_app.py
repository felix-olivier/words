from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

stub = {
    "words": [{
        "word": "impeachment",
        "definitions": ["Amerikaans recht: <br />het in staat van beschuldiging stellen, niet het afzetten, van een overheidsfunctionaris."]
    }, {
        "word": "halal",
        "definitions": ["Halal (Arabisch: حَلاَلْ: rein, toegestaan) is een islamitische term waarmee wordt aangegeven wat voor moslims toegestaan is.", "Halal staat voor alles wat door de Koran als goed en rein kan worden gezien."]
    }]
}

@app.route('/', methods=['GET'])
def get_stub():
    return jsonify(stub)

'''
Get the article text by scraping nos.nl
'''
def get_article_text(id):

    page = requests.get("http://nos.nl/l/" + str(id))
    soup = BeautifulSoup(page.content, 'html.parser')

    article_body = soup.find(class_="article_body row")
    paragraphs = article_body.find_all('p')

    article_text = ''
    for paragraph in paragraphs:
        article_text += ' ' + paragraph.get_text()

    print(article_text)
    return article_text

'''
Get a predefined list of difficult words
'''
def get_difficult_words():
    local = True
    if (local):
        file = open('app/data/words.csv', 'r')
    else:
        file = open('data/words.csv', 'r')
    difficult_words = file.read().split(',')
    file.close()
    return difficult_words

'''
TODO: Fetch the definition(s) of the difficult word
'''
def get_definitions(word):
    return ['none yet']

'''
remove all characters other than letters from string
'''
def cleanup_word(input):
    valids = []
    for character in input:
        if character.isalpha():
            valids.append(character)
    return ''.join(valids)
'''
Count the number of syllables in word
'''
def syllable_count(word): ## todo: this is up for improvement: written for english not dutch, what about oe, au, ui etc
    word = word.lower()
    count = 0
    vowels = "aeiouy"
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith("e"):
        count -= 1
    if count == 0:
        count += 1
    return count



'''
Basic word complexity analysis. A word is complex when one of the following is true:
    - Not capitalized (todo: exclude start of sentence)
    - word length > 10 characters
    - more than four syllables
    - word contains x, y, c, ch, ae, ea, q, z and word length > 6 characters
'''
def get_difficult_words_alternative(article_text):
    ### CONFIG
    max_word_length = 10
    max_syllables = 4
    danger_letters = ['x', 'y', 'c', 'ch', 'ae', 'ea', 'q', 'z']
    danger_letters_max_length = 6

    ### Functionality
    all_words = article_text.split()

    to_return = []
    for word in all_words: # todo: uniques

        word = cleanup_word(word)

        if (len(word) <= 0):
            continue
        elif (word[0].isupper()):
            continue # todo: up for improvement, word should not be skipped when at the start of a sentence
        elif (len(word) >= max_word_length):
            to_return.append(word)
        elif (syllable_count(word) >= max_syllables):
            to_return.append(word)
        elif (len(word) >= danger_letters_max_length):
            for danger_letter in danger_letters:
                if (danger_letter in word):
                    to_return.append(word)
                    break

    return set(list(to_return))


@app.route('/items/<int:id>')
def get_difficults_words(id):
    article_text = get_article_text(id)

    difficult_words = get_difficult_words_alternative(article_text) # this is based upon textual analysis
    # difficult_words = get_difficult_words() # this is based upon a pre-defined list

    words_to_explain = []
    for word in difficult_words:
        if (word in article_text):
            words_to_explain.append({
                'word': word,
                'definitions': get_definitions(word)
            })

    return jsonify({'words': words_to_explain})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
