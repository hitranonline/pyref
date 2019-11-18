import os
import sys
import django
import requests
import json
from urllib import request, parse  
from bs4 import BeautifulSoup 

from conf import webapp_path
sys.path.append(webapp_path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'pyref.settings'

django.setup()

from refs.models import Ref, get_ref_from_doi

class Bibtex(object):
    """ Convert doi number to get bibtex entries."""
    def __init__(self, doi=None, title=None):
        """Input doi number-- Returns doi, encoded doi, and doi url."""
        _base_url = "http://dx.doi.org/"
        self.doi = doi
        self.title = title
        self.bibtex = None
        if doi:
            self._edoi = parse.quote(doi)
            self.url = _base_url + self._edoi  
        else:
            self.url = None    

# Beautiful Soup is a Python library for pulling data out of HTML and XML files
    def _soupfy(self, url):
        """Returns a soup object."""
        html = request.urlopen(url).read()
        self.soup = BeautifulSoup(html)
        return self.soup                

# Get the ADS link for the paper   
    def getADS(self):
        """Get bibtex entry from doi using ADS database."""
        uri = "http://adsabs.harvard.edu/cgi-bin/basic_connect?qsearch="
        url = uri + self._edoi

# Make Beautiful Soup look for ADS Bibcode (which is necessary for retrieving the ADS link)
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
            self.bibtex = '\n'.join(bib[5:-1])
        finally:
            return self.bibtex
        
doi = '10.1103/PhysRevA.85.032515'
bib = Bibtex(doi)
print(bib.getADS())

