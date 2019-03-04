import nltk
import json
import re
from src.lib.clean import valid_tkn
from src.lib.web_api import web_get
from src.lib.helpers import levenshtein


def parse_tools(steps):
    tools_lst = []
    tools_kw = set([line.strip() for line in open('./src/lib/categories/ingredients/tools.txt')])

    for raw_step in steps:
        step = nltk.word_tokenize(raw_step)
        for s in step:
            if s in tools_kw:
                tools_lst.append(s)

        bigrams = [step[i:] for i in range(2)]
        bigrams = zip(*bigrams)
        bigrams = [" ".join(bigram) for bigram in list(bigrams)]

        for bigram in bigrams:
            if bigram in tools_kw:
                tools_lst.append(bigram)


    return list(set(tools_lst))

def parse_methods(steps):
    methods = []
    methods_kw = set([line.strip() for line in open('./src/lib/categories/ingredients/methods.txt')])
    methods2_kw = set([line.strip() for line in open('./src/lib/categories/ingredients/methods2.txt')])

    all_methods_kw = methods_kw | methods2_kw


    for raw_step in steps:
        step = nltk.word_tokenize(raw_step)
        for s in step:
            if s in all_methods_kw:
                methods.append(s)

        bigrams = [step[i:] for i in range(2)]
        bigrams = zip(*bigrams)
        bigrams = [" ".join(bigram) for bigram in list(bigrams)]

        for bigram in bigrams:
            if bigram in all_methods_kw:
                methods.append(bigram)

    # Remove duplicates
    return list(set(methods))


def split_steps(steps, ingredients, tools, methods):
    # TODO: add 'hr', 'min', 'second', 'sec' to time pattern
    timePattern = re.compile('(\d+ hour(?:s?) (?:and )?\d+ minute(?:s?))|(\d+ minute(?:s?))|(\d+ hour(?:s?))')
    temperaturePattern = re.compile('(\d+(?:(?: [dD]egrees)|(?:\u00b0)) (?:(?:[fF]ahrenheit)|(?:[fF])|(?:[Cc]elcius)|(?:[cC])))')

    new_steps = []
    for raw_step in steps:
        step = nltk.word_tokenize(raw_step)

        bigrams = [step[i:] for i in range(2)]
        bigrams = zip(*bigrams)
        bigrams = [" ".join(bigram) for bigram in list(bigrams)]

        new_step = {
            "ingredients": [],
            "tools": [],
            "methods": [],
            "times": [],
            "temperature": []
        }

        for s in step:
            if s in ingredients:
                new_step['ingredients'].append(s)
            if s in tools:
                new_step['tools'].append(s)
            if s in methods and s not in new_step['methods']:
                new_step['methods'].append(s)

        for bigram in bigrams:
            if bigram in ingredients:
                new_step['ingredients'].append(bigram)
            if bigram in tools:
                new_step['tools'].append(bigram)
            if bigram in methods and bigram not in new_step['methods']:
                new_step['methods'].append(bigram)
            if timePattern.match(bigram):
                new_step['times'].append(bigram)
            if temperaturePattern.match(bigram):
                new_step['temperature'].append(bigram)

        new_steps.append(new_step)

    return new_steps





