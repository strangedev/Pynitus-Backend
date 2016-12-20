import unicodedata


def NFD(text):
    return unicodedata.normalize('NFD', text)


def canonical_caseless(text):
    return NFD(NFD(text).casefold())


def unicode_compare(t1, t2):
    return canonical_caseless(t1) == canonical_caseless(t2)
