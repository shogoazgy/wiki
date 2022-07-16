import requests
import json
import pandas as pd
import MeCab
import math

from wordcloud import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer
import csv
import folium

class TextMining():
    def __init__(self):
        self.mecab = MeCab.Tagger ('~/usr/local/lib/mecab/dic/mecab-ipadic-neologdd')
    
    def text_normalize(self, text):
        text = ' '.join(text.splitlines())
        return text
    
    def word_separate(self, text, word_class=None):
        words = []
        node = self.mecab.parseToNode(text)
        if word_class is None:
            while node:
                words.append(node.surface)
                node = node.next
        else:
            while node:
                if node.feature.split(",")[0] in word_class:
                    words.append(node.surface)
                node = node.next
        return ' '.join(words)
    def word_cloud(self, words, img_file='wordcloud', font_path='~/Library/Fonts//Arial Unicode.ttf', stop_words=[], frequence = False):
        if frequence:
            wc = WordCloud(background_color='white', font_path=font_path, stopwords=stop_words, regexp=r"\w[\w']+").generate_from_frequencies(words)
        else:
            wc = WordCloud(background_color='white', font_path=font_path,  stopwords=stop_words, regexp=r"\w[\w']+").generate(words)
        wc.to_file(img_file + '.png')
        return
    def tf_idf(self, corpus):
        tfidf = TfidfVectorizer(corpus)
        return tfidf



    
if __name__=='__main__':
    texts = []
    text_test = []
    place_list = []
    tm = TextMining()
    with open('data.json', 'r') as f:
        data = json.load(f)
    for place in data:
        try:
            text = data[place]['lead'] + data[place]['overview']
            text = tm.text_normalize(text)
            data[place]['text'] = text
        except:
            try:
                text = data[place]['lead']
                text = tm.text_normalize(text)
                data[place]['text'] = text
            except:
                data[place]['text'] = ''
        try:
            words = tm.word_separate(data[place]['text'])
            texts.append(words)
            text_test.append(words)
            #tm.word_cloud(words, img_file=place)
        except:
            pass
        place_list.append(place)
    size = len(text_test)



    with open('tokyo.csv') as f:
        r = csv.reader(f)
        for row in r:
            text_tokyo = row[2] + row[3] + row[6]
            text_tokyo = tm.text_normalize(text_tokyo)
            text_separated = tm.word_separate(text_tokyo)
            texts.append(text_separated)
    tfidf_model = TfidfVectorizer(token_pattern='(?u)\\b\\w+\\b')
    tfidf_model.fit(texts)
    
    tfidf_test = tfidf_model.transform(text_test).toarray()
    for i in range(size):
        tfidf_dict = dict(zip(tfidf_model.get_feature_names(), tfidf_test[i]))
        tfidf_dict = {k: v for k, v in tfidf_dict.items() if v > 0}
        try:
            tm.word_cloud(tfidf_dict, img_file=place_list[i] + '_tfidf', frequence=True)
        except:
            pass
    
    