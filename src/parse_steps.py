import nltk
import json
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
    methods = {
        "primary_methods": [],
        "secondary_methods": []
    }
    methods_kw = set([line.strip() for line in open('./src/lib/categories/ingredients/methods.txt')])
    methods2_kw = set([line.strip() for line in open('./src/lib/categories/ingredients/methods2.txt')])


    for raw_step in steps:
        step = nltk.word_tokenize(raw_step)
        for s in step:
            if s in methods_kw:
                methods["primary_methods"].append(s)
            if s in methods2_kw:
                methods["secondary_methods"].append(s)

        bigrams = [step[i:] for i in range(2)]
        bigrams = zip(*bigrams)
        bigrams = [" ".join(bigram) for bigram in list(bigrams)]

        for bigram in bigrams:
            if bigram in methods_kw:
                methods["primary_methods"].append(bigram)
            if bigram in methods2_kw:
                methods["secondary_methods"].append(bigram)

    # Remove duplicates
    methods["primary_methods"] = list(set(methods["primary_methods"]))
    methods["secondary_methods"] = list(set(methods["secondary_methods"]))
    return methods


def parse_steps(steps):
    timePattern = re.compile('(\d+ hour(?:s?) (?:and )?\d+ minute(?:s?))|(\d+ minute(?:s?))|(\d+ hour(?:s?))')
    temperaturePattern = re.compile('(\d+(?:(?: [dD]egrees)|(?:\u00b0)) (?:(?:[fF]ahrenheit)|(?:[fF])|(?:[Cc]elcius)|(?:[cC])))')

    pass


