from django.test import TestCase

#class DOIResolveTest(TestCase):
    
#        def test_resolving_doi_populates_add_reference_page(self):
#            doi = input("Enter doi Here: ")
#            url = '/refs/resolve/?doi=' + doi
#            response = self.client.get(url)
            
#            self.assertContains(response,
#        r'<input type="text" name="journal" value="Physical Review A" =axlength="500" id="id_journal" />',html=True)

import os
import sys
import django

webapp_path = os.path.join('/Users/fskin/djangohitran')
sys.path.append(webapp_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'pyref.settings'
django.setup()
from refs.models import Ref, get_ref_from_doi

# Create your tests here.
import gscholar 
#from gscholar import query
import requests
import json
#import html
#from html.entities import html5 as _html5
#import re
#import sys
import httplib2
import bs4
import argparse
from urllib import request, parse  
#from urllib.error import HTTPError
from bs4 import BeautifulSoup  

#########This section will get you the BibTeX Title for the reference without ADS###############
class Bibtex(object):
    """ Convert doi number to bibtex entries."""
    def __init__(self, doi=None, title=None):
        """
        Input doi number ou title (actually any text/keyword.)
        Returns doi, encoded doi, and doi url or just the title.
        """
        _base_url = "http://dx.doi.org/"
        self.doi = doi
        self.title = title
        self.bibtex = None
        if doi:
            self._edoi = parse.quote(doi)
            self.url = _base_url + self._edoi  # Encoded doi.
        else:
            self.url = None

    def _soupfy(self, url):
        """Returns a soup object."""
        html = request.urlopen(url).read()
        self.soup = BeautifulSoup(html, 'html.parser')
        return self.soup
 
    def getADS(self):
        """Get bibtex entry from doi using ADS database."""
        uri = "http://adsabs.harvard.edu/cgi-bin/basic_connect?qsearch="
        url = uri + self._edoi

        soup = self._soupfy(url)
        try:
            tag = soup.findAll('input', attrs={"name": "bibcode"})[0]
        except IndexError:
            print("\nADS failed\n")
        else:
            bibcode = tag.get('value') if tag.get('value') else None
            uri = 'http://adsabs.harvard.edu/cgi-bin/nph-bib_query?bibcode='
            end = '&data_type=BIBTEX&db_key=AST%26nocookieset=1'
            url = uri + bibcode + end
            bib = request.urlopen(url).read().decode('utf-8')
            bib = bib.split('\n')

            self.bibtex = '\n'.join(bib[7:-14]) #[5:-14] #[5:-16]
        finally:
            return self.bibtex
    
    
    def getGScholar(self):
        bibtex = query(self._edoi, 4)[0] 
        self.bibtex = bibtex  #.decode('utf-8')
        return self.bibtex

def main(argv=None):
    if argv is None:
        argv = sys.argv

    args = parse_args(argv[1:])

    doi = args.positional
    method = args.method

    def allfailed():
        """All failed message+google try."""
        bold, reset = "\033[1m", "\033[0;0m"
        bib.getGScholar()
        url = bold + bib.url + reset
        msg = """Unable to resolve this DOI using database
        \nTry opening, \n\t{0}\nand download it manually.
        \n...or if you are lucky check the Google Scholar search below:
        \n{1}
        """.format(url, bib.bibtex)
        return msg

    bib = Bibtex(doi=doi)

doi = input("Enter doi Here: ") 
#doi = '10.1103/PhysRevA.85.032515'
bib = Bibtex(doi)
title = bib.getADS()
print(title)

#########This section will get you the HTML Title for the Reference without ADS###############
def escape2(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace("$^{", "<SUP>") # Must be done first!
    s = s.replace("}$", "</SUP>")
    s = s.replace("{", "")
    s = s.replace("}", "")
    s = s.replace("\"", "")
    s = s.replace("'", "")
    s = s.replace("''", "")
    return s
#escape2( """& < " '> """ )
print(escape2("{}".format(title)))
