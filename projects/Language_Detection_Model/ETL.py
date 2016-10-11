import os
import glob
import re
import string
import codecs
import numpy as np

langs = [d for d in os.listdir('txt') if len(d) == 2]
# classes = dict(zip(langs, range(len(langs))))

# read lines, remove tag, numbers and punctuations
p = re.compile(r'(<.*?>|[\d\t]|[{}])'.format(re.escape(string.punctuation)), flags=re.UNICODE)


def extract_training_data(n_lines):
    fo = codecs.open('txt/train.txt', 'w', encoding='utf-8')
    for lang in langs:
        i = 0
        files = glob.glob(os.path.join('txt', lang, '*.txt'))
        # randomly choose files in the directory
        indices = np.random.random_sample(len(files))
        file_dict = dict(zip(range(len(files)), files))
        while i < n_lines:
            index = indices.pop()
            fpath = file_dict[index]
            with codecs.open(fpath, 'r', encoding='utf-8') as fi:
                for line in fi:
                    line = p.sub('', line.rstrip())
                    if line:
                        fo.write(lang + '\t' + line + '\n')
                        i += 1
    fo.close()


def extract_test_data():
    with codecs.open('txt/test.txt', 'w', encoding='utf-8') as fo:
        with codecs.open('europarl.test', 'r', encoding='utf-8') as fi:
            for line in fi:
                fo.write(p.sub('', line))


extract_training_data(5000)
extract_test_data()
