import pandas as pd
import nltk
import re
import math
import pymorphy2 as pm
import os
morph = pm.MorphAnalyzer()

texts_directory = './texts/'
# texts: https://www.kaggle.com/oldaandozerskaya/fiction-corpus-for-agebased-text-classification/?select=train

tikhonov = pd.read_csv('https://raw.githubusercontent.com/h3ic/cheto/main/komplingva/tikhonov.csv')
tikh_dict = list(tikhonov.word)
tikh_morphs = list(tikhonov.n_morph)


def get_index(text):
    text = re.sub('[А-Я][а-я]+', '', text)
    text = text.lower()
    text = re.sub('[^\-\w\s]', '', text)
    words = nltk.word_tokenize(text)
    words_lem = [morph.parse(word)[0].normal_form for word in words]
    words_lem = [re.sub('ё', 'е', word) for word in words_lem]

    n_words = len(words_lem)
    n_morphs = 0
    undef_words = 0

    for i, word in enumerate(words_lem):
        if word in tikh_dict:
            morph_in_word = tikh_morphs[i]
            n_morphs += morph_in_word
        elif len(word) < 5 or not word.isalpha():
            continue
        else:
            undef_words += 1

    morph_mean = math.floor(n_morphs/n_words)
    n_morphs += undef_words*morph_mean
    synth_index = n_morphs/n_words

    return synth_index


text_indices = []

for filename in os.listdir(texts_directory):
    file = open(texts_directory + filename, 'r')
    text = file.read()
    file.close()
    index = get_index(text)
    print(index)
    text_indices.append(index)

print('the index is ', text_indices/len(text_indices))