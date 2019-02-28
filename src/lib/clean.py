import re

def valid_tkn(tkn, sw, kw):
    if tkn in sw:
        # stopwords
        return False
    elif tkn in kw:
        # keywords
        return True
    elif not len(re.sub('[^a-zA-Z]','', tkn)):
        # only punctuation
        return False
    return True