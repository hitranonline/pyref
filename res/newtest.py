from django.test import TestCase

#class DOIResolveTest(TestCase):
    
 #       def test_resolving_doi_populates_add_reference_page(self):
 #           doi = input("Enter doi Here: ") #10.1103/PhysRevA.85.032515
  #          url = '/refs/resolve/?doi=' + doi
 #           response = self.client.get(url)
            
 #           self.assertContains(response,
 #       r'<input type="text" name="journal" value="Physical Review A" =axlength="500" id="id_journal" />',html=True)

# Create your tests here.
import os
import sys
import django
import requests
import json
import urllib.request
from urllib.error import HTTPError
import html
import re
import logging
from bs4 import BeautifulSoup  
from html.entities import name2codepoint  
from urllib.request import quote, Request, urlopen

from conf import webapp_path
sys.path.append(webapp_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'pyref.settings'
django.setup()

from refs.models import Ref, get_ref_from_doi

##########Code from Models#######################################################################
def get_citeproc_authors(cpd_author):
    if cpd_author is None:
        return None
    names = []
    for author in cpd_author:
        try:
            family = author['family'].title()
        except KeyError:
            name = author['name']
            names.append(name)
            continue
        try:
            given = author['given']
        except KeyError:
            # This author has first name
            names.append(family)
            continue
        initials = given.split()
        initials[0] = '{}.'.format(initials[0][0])
        initials = ' '.join(initials)
        names.append('{} {}'.format(initials, family))
    return ', '.join(names)

def parse_citeproc_json(citeproc_json):
    """Parse the provided JSON into a Ref object."""
    
    cpd = json.loads(citeproc_json)
    try:
        if cpd['type'] != 'article-journal':
            return None
    except KeyError:
        return None

    authors = get_citeproc_authors(cpd.get('author', ''))
    title = cpd.get('title', '').replace('\n', '')
    journal = cpd.get('container-title', '')
    volume = cpd.get('volume', '')
    page_start, page_end = cpd.get('page', ''), ''
    if page_start and '-' in page_start:
        page_start, page_end = page_start.split('-')
    article_number = cpd.get('article-number', '')
    doi = cpd.get('DOI', '')
    url = cpd.get('URL', '')
    try:
        year = cpd['issued']['date-parts'][0][0]
    except (KeyError, IndexError):
        year = None
        
    try:
        bibcode = cpd.get('bibcode', '')
    except (KeyError, IndexError):
        bibcode = None
        
# # =============================================================================
# #   OUTPUT
# # =============================================================================
    ref = [authors, 
        title, 
        journal, 
        volume,
        year, 
        page_start, 
        page_end, 
        doi,
        url, 
        article_number,
        citeproc_json]
    return ref 

def get_citeproc_json_from_doi(doi):
    base_url = 'http://dx.doi.org/'
    url = base_url + doi
    req = urllib.request.Request(url)
    req.add_header('Accept', 'application/citeproc+json')
    try:
        with urllib.request.urlopen(req) as f:
            citeproc_json = f.read().decode()
    except HTTPError as e:
        if e.code == 404:
            raise ValueError('DOI not found.')
        raise
    return citeproc_json

def get_source_from_doi(doi):
    citeproc_json = get_citeproc_json_from_doi(doi)
    ref = parse_citeproc_json(citeproc_json)
    return ref


#########This section will get you the Bibcode for the ADS sections to run properly###############
doi = input("Enter DOI Here: ")
doi_fetched = get_source_from_doi(doi)

ads_token = 'Enter Token Here'
token     = ads_token

rdoi = doi

rdoi_bs = rdoi.replace("\\", "%2F")    # Remove backslash and replace with URL code for backslash
rdoi_fs = rdoi_bs.replace("/", "%2F")  # Remove forwardslash and replace with URL code for backslash

rurl = requests.get("https://api.adsabs.harvard.edu/v1/search/query?q=doi:"+rdoi_fs,\
                 params={"q":"*:*", "fl": "*", "rows":2000},
                 headers={'Authorization': 'Bearer ' + token})

todos          = json.loads(rurl.text)
todos_response = todos.get('response', '')

    
Bibcode =  (todos_response['docs'][0]['bibcode']) 

print(Bibcode)

##########################This section uses ADS to get the LaTeX encoded Title##########################
token="Enter Token Here"
payload = {"bibcode": ["{}".format(Bibcode)],
           "sort": "first_author asc",
           "format": 
           '''{"ref_json": {"encoder": "%ZEncoding:latex\\bibitem",
              "title": "%T"}}'''
              }
r = requests.post("https://api.adsabs.harvard.edu/v1/export/custom", \
                 headers={"Authorization": "Bearer " + token, "Content-type": "application/json"}, \
                 data=json.dumps(payload))
response_json = r.json()
print('-'*72)
print(response_json['export']) 
print('-'*72)
ref_json = json.loads(response_json['export'])['ref_json']

print('title bibtex:', ref_json['title'])

####################This section uses ADS to get the html encoded title######################

payload = {"bibcode": ["{}".format(Bibcode)],
           "sort": "first_author asc",
           "format":
           '''{"ref_json": {"title": "%T"}}'''
              }
r = requests.post("https://api.adsabs.harvard.edu/v1/export/custom", \
                 headers={"Authorization": "Bearer " + token, "Content-type": "application/json"}, \
                 data=json.dumps(payload))
response_json = r.json()
ref_json = json.loads(response_json['export'])['ref_json']

print('title html:', ref_json['title'])












