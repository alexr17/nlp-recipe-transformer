import nltk
import json
import re
from src.lib.clean import valid_tkn

def parse_tools(steps):
    '''
    Parses the tools from the steps in a recipe
    '''
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
    '''
    Parses the methods from the steps in a recipe
    '''
    methods = {
        "primary_methods": [],
        "secondary_methods": []
    }
    methods_kw = set([line.strip() for line in open('./src/lib/categories/ingredients/methods.txt')])
    methods2_kw = set([line.strip() for line in open('./src/lib/categories/ingredients/methods2.txt')])

    all_methods_kw = methods_kw | methods2_kw


    for raw_step in steps:
        step = nltk.word_tokenize(raw_step)
        for s in step:
            if s in methods_kw:
                methods['primary_methods'].append(s)
            if s in methods2_kw:
                methods['secondary_methods'].append(s)

        bigrams = [step[i:] for i in range(2)]
        bigrams = zip(*bigrams)
        bigrams = [" ".join(bigram) for bigram in list(bigrams)]

        for bigram in bigrams:
            if bigram in methods_kw:
                methods['primary_methods'].append(bigram)
            if bigram in methods2_kw:
                methods['secondary_methods'].append(bigram)

    # Remove duplicates
    methods['primary_methods'] = list(set(methods['primary_methods']))
    methods['secondary_methods'] = list(set(methods['secondary_methods']))
    return methods


def split_steps(steps, ingredients, tools, methods):
    '''
    Parses the steps
    '''
    # TODO: add 'hr', 'min', 'second', 'sec' to time pattern
    timePattern = re.compile('(\d+ hour(?:s?) (?:and )?\d+ minute(?:s?))|(\d+ minute(?:s?))|(\d+ hour(?:s?))')
    temperaturePattern = re.compile('(\d+(?:(?: [dD]egrees)|(?:\u00b0)))')


    methods = list(set(methods['primary_methods']) | set(methods['secondary_methods']))
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
            "temperature": [],
            "raw_step": raw_step
        }

        for s in step:
            if s in ingredients and s not in new_step['ingredients']:
                new_step['ingredients'].append(s)
            if s in tools and s not in new_step['tools']:
                new_step['tools'].append(s)
            if s in methods and s not in new_step['methods']:
                new_step['methods'].append(s)

        for bigram in bigrams:
            if bigram in ingredients and bigram not in new_step['ingredients']:
                new_step['ingredients'].append(bigram)
            if bigram in tools and bigram not in new_step['tools']:
                new_step['tools'].append(bigram)
            if bigram in methods and bigram not in new_step['methods']:
                new_step['methods'].append(bigram)
            if timePattern.match(bigram):
                new_step['times'].append(bigram)
            if temperaturePattern.match(bigram):
                new_step['temperature'].append(bigram + ' F')

        new_steps.append(new_step)

    return new_steps
