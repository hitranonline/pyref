import os
import sys
import django
import requests
import json
from urllib import request, parse  

webapp_path = os.path.join('/Users/fskin/pyref')
sys.path.append(webapp_path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'pyref.settings'

django.setup()

from refs.models import Ref, get_ref_from_doi

from html.entities import html5 as _html5
import html

s = html.escape( """& < " '> """ )   # s = '&amp; &lt; &quot; &#x27; &gt;'
html.escape(s, quote=True)

html.escape("{authors: Zhang, S. B. and D. L. Yeager\
title: Complex-scaled multireference configuration-interaction method to study Be and Be-like cations' (B, C, N, O, Mg) Auger resonances 1s2s<SUP>2</SUP>2p <SUP>1,3</SUP>P<SUP>o</SUP>\
journal: Physical Review A\
volume: 85\
start-page: 032515\
end-page: %P\
year: 2012\
doi: 10.1103/PhysRevA.85.032515\
bibcode: https://ui.adsabs.harvard.edu/abs/2012PhRvA..85c2515Z}")