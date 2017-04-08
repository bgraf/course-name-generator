#!/usr/bin/env python3

# Course name generator.
# - generates sciency course names.
#
# 2017, bgraf
# License: MIT

import argparse
import random

WORDS_BY_KIND = {
    'adjective': ['anthropological',
                  'advanced',
                  'applied',
                  'central',
                  'chemical',
                  'classic',
                  'clinical',
                  'comparative',
                  'complex',
                  'molecular',
                  'practical',
                  'quantitative',
                  'qualitative',
                  'dynamic',
                  'functional',
                  'embedded',
                  'evolutionary',
                  'foreign',
                  'heterodox',
                  'inorganic',
                  'international',
                  'linear',
                  'medical',
                  'modern',
                  'modular',
                  'naval',
                  'nonlinear',
                  'organic',
                  'parallel',
                  'physical',
                  'planetary',
                  'political',
                  'popular',
                  'radical',
                  'safety-critical',
                  'sequential',
                  'social',
                  'socialist',
                  'structural',
                  'systemic',
                  'tectonic',
                  'theoretical'],
    'introduction': ['effects of',
                     'introduction to',
                     'perspectives on',
                     'foundations of',
                     'the nature of'],
    'listener': ['biologist',
                 'physicist',
                 'statistician',
                 'architect',
                 'computer scientist',
                 'physician',
                 'educator',
                 'astronomer',
                 'chemist',
                 'engineer',
                 'pharmacist',
                 'philosopher',
                 'psychologist',
                 'economist',
                 'linguist'],
    'prefix': ['astro', 'hydro', 'aero', 'auto', 'tele', 'geo', 'macro', 'micro'],
    'compound_front': ['model',
                       'rule',
                       'economy',
                       'science',
                       'population',
                       'computer',
                       'network',
                       'fluid',
                       'space',
                       'market'],
    'topic': ['economics',
              'sciences',
              'dynamics',
              'populations',
              'physics',
              'modelling',
              'statistics',
              'analysis',
              'ideologies',
              'programming',
              'chemistry',
              'algorithmics',
              'architecture',
              'systems',
              'languages',
              'archaeology',
              'theory',
              'policies',
              'philosophy',
              'physiology',
              'finance',
              'evolution',
              'algebra'],
    'compound_back': ['driven', 'based', 'derived']}


class CourseNameGenerator:
    PROBABILITIES = {
        'introduction': 0.2,
        'adjective': 0.9,
        'compound_front': 0.15,
        'prefix': 0.4,
        'topic': 1.0,
        'listener': 0.2,
        'compound_back': 1.0,
        'person_prefix': 0.1,
        'num': 0.2
    }

    def __init__(self, word_file=None, words_by_kind=None, seed=None):
        if word_file is None and words_by_kind is None:
            raise RuntimeError('neither word_file nor words_by_kind supplied')
        if word_file is not None and words_by_kind is not None:
            raise RuntimeError(
                'word_file and words_by_kind supplied, choose one')

        if word_file is not None:
            self.words_by_kind = {}
            with open(word_file) as f:
                for line in f.readlines():
                    kind, word = line.strip().split(sep=',', maxsplit=2)
                    if kind not in self.words_by_kind:
                        self.words_by_kind[kind] = []
                    self.words_by_kind[kind].append(word)
        else:
            self.words_by_kind = words_by_kind

        # setup RNGs
        seed = random.randint(3, 2 ** 30) if seed is None else seed
        self.rngs = {
            kind: random.Random(x=seed + i) for i, kind in enumerate(self.PROBABILITIES.keys())
        }
        self.rngs['person_prefix'] = random.Random(x=seed - 2)
        self.rngs['which_num'] = random.Random(x=seed - 3)

    def gen_course_name(self):
        def matches(key):
            return self.PROBABILITIES[key] >= self.rngs[key].random()

        def sample(key):
            return self.rngs[key].sample(self.words_by_kind[key], 1)[0]

        title = []
        if matches('introduction'):
            title.append(sample('introduction'))

        if matches('adjective'):
            title.append(sample('adjective'))

        if matches('compound_front'):
            title.append('{}-{}'.format(sample('compound_front'),
                                        sample('compound_back')))

        title.append((sample('prefix') if matches(
            'prefix') else '') + sample('topic'))

        if matches('listener'):
            prefix = sample('prefix') if matches('person_prefix') else ''

            title.append('for {}{}s'.format(prefix, sample('listener')))

        if matches('num'):
            title.append(self.rngs['which_num'].sample(
                ['I', 'I' * 2, 'I' * 3], 1)[0])

        title[0] = title[0].capitalize()
        return ' '.join(title)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--number', type=int, default=1,
                        help='number of titles to generate')
    parser.add_argument('-w', '--words', type=str, default=None,
                        help='word file')

    args = parser.parse_args()

    if args.words is not None:
        gen = CourseNameGenerator(word_file=args.words)
    else:
        gen = CourseNameGenerator(words_by_kind=WORDS_BY_KIND)

    for _ in range(args.number):
        print(gen.gen_course_name())


if __name__ == '__main__':
    main()
