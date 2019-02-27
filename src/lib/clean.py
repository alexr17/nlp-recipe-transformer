

def valid_tkn(tkn, sw, kw):
    if tkn in sw:
        return False
    elif tkn in kw:
        return True

    return True