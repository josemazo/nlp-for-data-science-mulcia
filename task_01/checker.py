import collections
import dill
import os
import re

import constants


class Checker(object):

    keyboard_error_multiplier = 1.5
    bigram_multiplier = 2

    def __init__(self, data_files_path='data_files',
                 pickle_filename='checker_model.pkl'):

        self.keyboard_errors = list()

        if os.path.isfile(pickle_filename):
            with open(pickle_filename, 'rb') as pickle_file:
                self.model = dill.load(pickle_file)

        else:
            self.last_index = 0
            self.model = dict()
            self.model['text'] = list()
            self.model['freq_dist'] = collections.defaultdict(lambda: 1)
            self.model['indexed_text'] = collections.defaultdict(lambda: [])

            for filename in os.listdir(data_files_path):
                filename = os.path.join(data_files_path, filename)

                if os.path.isfile(filename):
                    with open(filename, 'r', encoding='utf-8') as data_file:
                        for line in data_file:
                            line = self.words(line)
                            self.train(line)

            with open(pickle_filename, 'wb') as pickle_file:
                dill.dump(self.model, pickle_file)

    def train(self, features):
        current_index = self.last_index

        self.model['text'].extend(features)
        for index, feature in enumerate(features):
            self.model['freq_dist'][feature] += 1
            self.model['indexed_text'][feature].append(index + current_index)

        self.last_index += len(features)

    def correct(self, pre, word, post):
        candidates = self.known([word], self.model['freq_dist']) or self.known(
            self.edits1(word), self.model['freq_dist']) or self.known_edits2(
            word, self.model['freq_dist']) or [word]

        keyboard_errors = self.get_keyboard_errors(word)

        bigrams_data = self.get_bigrams(candidates, pre, post,
                                        self.model['text'],
                                        self.model['indexed_text'])

        if bigrams_data:
            candidates = {c: self.model['freq_dist'][c]
                          for c in candidates}

            for candidate, multiplier in bigrams_data.items():
                candidates[candidate] *= multiplier

            # candidates = sorted(candidates.keys(), key=candidates.get)[::-1]
            candidates = sorted(candidates.keys(),
                                key=lambda x: self.apply_keyboard_error(
                                    keyboard_errors, candidates, x))[::-1]

        else:
            # candidates = sorted(candidates,
            #                     key=self.model['freq_dist'].get)[::-1]
            candidates = sorted(candidates,
                                key=lambda x: self.apply_keyboard_error(
                                    keyboard_errors,
                                    self.model['freq_dist'], x))[::-1]

        return candidates

    @classmethod
    def words(cls, text):
        return re.findall(constants.REGEX, text.lower())

    @classmethod
    def edits1(cls, word):
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [a + b[1:] for a, b in splits if b]
        transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b) > 1]
        replaces = [a + c + b[1:] for a, b in splits
                    for c in constants.ALPHABET if b]
        inserts = [a + c + b for a, b in splits for c in constants.ALPHABET]

        return set(deletes + transposes + replaces + inserts)

    @classmethod
    def known_edits2(cls, word, freq_dist):
        return set(e2 for e1 in cls.edits1(word) for e2 in cls.edits1(e1)
                   if e2 in freq_dist)

    @classmethod
    def known(cls, words, freq_dist):
        return set(w for w in words if w in freq_dist)

    @classmethod
    def get_keyboard_errors(cls, word):
        keyboard_errors = list()
        for i in range(len(word)):
            for letter in constants.KEYBOARD_CLOSENESS[word[i]]:
                alt_word = list(word)
                alt_word[i] = letter
                alt_word = ''.join(alt_word)
                keyboard_errors.append(alt_word)

        return keyboard_errors

    @classmethod
    def apply_keyboard_error(cls, keyboard_errors, dictionary, candidate):
        if candidate in keyboard_errors:
            try:
                return dictionary[candidate] * cls.keyboard_error_multiplier
            except OverflowError:
                return float('inf')

        else:
            return dictionary[candidate]

    @classmethod
    def get_bigrams(cls, candidates, pre, post, text, indexed_text):
        bigrams_data = None

        if pre or post:
            length = len(text)
            bigrams_data = collections.defaultdict(lambda: 1)
            for candidate in candidates:
                indices = indexed_text[candidate]

                if pre:
                    for i in indices:
                        if i > 0:
                            pre_candidate = text[i - 1]
                            if pre_candidate == pre:
                                try:
                                    bigrams_data[
                                        candidate] *= cls.bigram_multiplier
                                except OverflowError:
                                    bigrams_data[
                                        candidate] = float('inf')

                if post:
                    for i in indices:
                        if i < length - 2:
                            post_candidate = text[i + 1]
                            if post_candidate == post:
                                try:
                                    bigrams_data[
                                        candidate] *= cls.bigram_multiplier
                                except OverflowError:
                                    bigrams_data[
                                        candidate] = float('inf')

        return bigrams_data
