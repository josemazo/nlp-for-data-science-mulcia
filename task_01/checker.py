# -*- coding: utf-8 -*-

import collections
import dill
import re

"""
Shit came to me. I deleted this file in a good version of it. :_(
Work for tomorrow:
- Put all of this in class. As before.
- Paremetrize paths and filenames.
- Read files from a directory. As before.
- Contruct the model line by line.
- Use dill for creating or loading a pickle with the model.
- Accept 3 paramenters in correct().
- Use 3-grams for correct() (Feature not developed before).
- Add error by closeness in the keyboard (Feature not developed before).
"""


class Checker(object):
    pass


def words(text):
    return re.findall('[a-zñáéíóúü]+', text.lower())


def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

NWORDS = train(words(open('big.txt', 'r', encoding='utf-8').read()))

alphabet = 'abcdefghijklmnopqrstuvwxyzñáéíóúü'


def edits1(word):
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b) > 1]
    replaces = [a + c + b[1:] for a, b in splits for c in alphabet if b]
    inserts = [a + c + b for a, b in splits for c in alphabet]
    return set(deletes + transposes + replaces + inserts)


def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)


def known(words):
    return set(w for w in words if w in NWORDS)


def correct(word):
    candidates = known([word]) or known(
        edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=NWORDS.get)
