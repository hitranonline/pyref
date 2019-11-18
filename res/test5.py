import os
import sys
import django
import requests
import json
from urllib import request, parse  
from bs4 import BeautifulSoup 
import gscholar 

webapp_path = os.path.join('/Users/fskin/pyref')
sys.path.append(webapp_path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'pyref.settings'

django.setup()

from refs.models import Ref, get_ref_from_doi

s = "Zhang, S. B."
words = s.split(' ') 
string =[] 
for word in words: 
    string.insert(-1, word) 
print(" ".join(string))