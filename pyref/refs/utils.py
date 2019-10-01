import re

def ensure_https(url):
    if url.startswith('https'):
        return url
    if url.startswith('http'):
        return 'https' + url[4:]
    return 'https://' + url

def canonicalize_doi(doi):
    """Remove https://dx.doi.org/ etc. from start of string doi."""
    patt = '^https?:\/\/(?:dx\.)?doi\.org/'
    return re.sub(patt, '', doi)
