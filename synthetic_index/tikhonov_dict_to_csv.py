import re
import pandas as pd

origin = open('tikhonov-utf8.txt', 'r')
dest = open('tikhonov.csv', 'w')
dest.write('word,n_morph\n')


def get_n_morph(line):
    line = re.sub("'", '', line)
    morph_part = re.search(r'(?<= \| )(\w+\S+)+', line)[0]
    n_morph = morph_part.count('/')
    return n_morph


for line in origin:
    try:
        _ = re.match(r'(\w+\.)', line)[0]
        continue

    except TypeError:
        word = re.match(r'(\S+)', line)[0]
        if word[-1].isalpha():
            n_morph = get_n_morph(line)

        elif word[-1] == '1':
            word = word[:-1]
            n_morph = get_n_morph(line)

        elif word[-1] != '1':
            continue

        else:
            raise NameError('wow')

    dest.write(word + ',' + str(n_morph) + '\n')
    
origin.close()
dest.close()