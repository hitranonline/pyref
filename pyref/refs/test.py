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
from refs.models import Ref, get_ref_from_doi
import gscholar 
import requests
import json
import httplib2
import bs4
import argparse
from urllib import request, parse  
from bs4 import BeautifulSoup  
from models_v2 import *

webapp_path = os.path.join('/Users/fskin/djangohitran')
sys.path.append(webapp_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'pyref.settings'
django.setup()

#########This section will get you the Bibcode for the ADS sections to run properly###############
doi = input("Enter DOI Here: ")
doi_fetched = get_source_from_doi(doi)

ads_token = '4PtdkIDyxpjjZ1JDYJ4HI59VXJuJD98tACcrnfPv'
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
token="gx43LyUuTTD0zoTWx8qKpWbWi3euTmx7FCM3fJjY"
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












