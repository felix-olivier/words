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

    return article_text

'''
Get a predefined list of difficult words
'''
def get_difficult_words():
    file = open('data/words.csv', 'r')
    difficult_words = file.read().split(',')
    file.close()
    return difficult_words

'''
TODO: Fetch the definition(s) of the difficult word
'''
def get_definitions(word):
    return ['none yet']


@app.route('/items/<int:id>')
def get_difficults_words(id):
    article_text = get_article_text(id)

    difficult_words = get_difficult_words()

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
