{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# **A Guide to creating citations using only a DOI**\n",
    "*Note: This Notebook seeks to retrieve citations for papers as 3 outputs; JSON, BibTeX and HTML. The citations in this notebook are retrieving the following information on a paper: Title, Authors, Journal Name, Volume Number, Page Range, Year, Hyperlink(s) to the Article and DOI of the Article. If you are looking for more detailed citations or other outputs then please refer to step 3 after steps 1 & 2!*\n",
    "\n",
    "<font color=blue>Step 1. Get DOI of the paper you want to cite</font> <br>\n",
    "<font color=red>Step 2. Use DOI to search in GScholar method -- Enter DOI in \"Enter Here\" in GScholar Method -- Output will be the full citation in BibTeX format, and the Bibcode for the paper will be displayed</font> <br>\n",
    "<font color=green>Step 3. Use Bibcode to search in ADS method -- Enter Bibcode in \"Enter Here\" in ADS Method -- Output is customizable, all formats possible. This method includes links to paper by DOI url & ADS url</font> <br>\n",
    "<font color=magenta>Note. (This May Happen to Some Users) Error! My paper was not in ADS! There is no Bibcode for the paper! -- Move to Step 4</font> <br>\n",
    "<font color=purple>Step 4. Use DOI to search in Urllib method -- Enter DOI in \"Enter Here\" in Urllib Method -- Output will be the full citation as a JSON output. Output is customizable as HTML through Step 5, or in BibTeX format through Step 6</font> <br>\n",
    "<font color=teal>Step 5. Enter the full JSON output in \"Enter Here\" to encode it as HTML</font> <br>\n",
    "<font color=maroon>Step 6. Enter DOI in \"Enter Here\" to retrieve the BibTeX citation for the paper</font> <br>\n",
    "\n",
    "### *All Done!* Now you have the citation for your paper in 3 different formats!"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## <font color=blue>Step 1.</font>\n",
    "\n",
    "<font color=blue>You can retrieve the DOI for your paper in many different ways.\n",
    "1. The DOI is a unique alphanumeric string assigned by the International DOI Foundation, to identify content and provide a persistent link to its location on the Internet. It is written in the general format of '10.1000/xyz123'\n",
    "2. The DOI should be written on the top left or top right corner of your paper, it is written as 'DOI:10.1000/xyz123'\n",
    "3. The DOI should be listed in the details or citation section on the publishers website where you have found your paper\n",
    "4. The DOI may also be written as a link, next to the papers information on the publishers website, the link is written as https://doi.org/10.1000/xyz123 or https://dx.doi.org/10.1000/xyz123\n",
    "5. In order to use this notebook please type in \"ENTER HERE\" spots the DOI in the '10.1000/xyz123' format, *NOT* as hyperlink</font>"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## <font color=red>Step 2. GScholar Method</font>"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "# This is the code to retrieve the citation. \n",
    "# Below this cell is an example of retrieving the citation using an example DOI and a Prompt to Enter your DOI!\n",
    "\n",
    "# Import these modules, install them if needed (you may need to 'pip install gscholar')\n",
    "from urllib import request, parse  \n",
    "# The urllib.request module defines functions and classes which help in opening URLs (mostly HTTP)\n",
    "# allows you to send HTTP/1.1 requests, without the need for manual labor\n",
    "# There’s no need to manually add query strings to your URLs, or to form-encode your POST data. HTTP connection pooling are 100% automatic, thanks to urllib3.\n",
    "from bs4 import BeautifulSoup \n",
    "# Beautiful Soup is a Python library for pulling data out of HTML and XML files. \n",
    "import gscholar \n",
    "# This package provides a python package and CLI to query google scholar and get references in various formats\n",
    "\n",
    "# Classifing the BibTex Object to get a BibTeX output format\n",
    "class Bibtex(object):\n",
    "    \"\"\" Convert doi number to get bibtex entries.\"\"\"\n",
    "    def __init__(self, doi=None, title=None):\n",
    "        \"\"\"Input doi number-- Returns doi, encoded doi, and doi url.\"\"\"\n",
    "        _base_url = \"http://dx.doi.org/\"\n",
    "        self.doi = doi\n",
    "        self.title = title\n",
    "        self.bibtex = None\n",
    "        if doi:\n",
    "            self._edoi = parse.quote(doi)\n",
    "            self.url = _base_url + self._edoi  \n",
    "        else:\n",
    "            self.url = None    \n",
    "\n",
    "# Beautiful Soup is a Python library for pulling data out of HTML and XML files\n",
    "    def _soupfy(self, url):\n",
    "        \"\"\"Returns a soup object.\"\"\"\n",
    "        html = request.urlopen(url).read()\n",
    "        self.soup = BeautifulSoup(html)\n",
    "        return self.soup                \n",
    "\n",
    "# Get the ADS link for the paper   \n",
    "    def getADS(self):\n",
    "        \"\"\"Get bibtex entry from doi using ADS database.\"\"\"\n",
    "        uri = \"http://adsabs.harvard.edu/cgi-bin/basic_connect?qsearch=\"\n",
    "        url = uri + self._edoi\n",
    "\n",
    "# Make Beautiful Soup look for ADS Bibcode (which is necessary for retrieving the ADS link)\n",
    "        soup = self._soupfy(url)\n",
    "        try:\n",
    "            tag = soup.findAll('input', attrs={\"name\": \"bibcode\"})[0]\n",
    "        except IndexError:\n",
    "            print(\"\\nADS failed\\n\")\n",
    "        else:\n",
    "            bibcode = tag.get('value') if tag.get('value') else None\n",
    "            uri = 'http://adsabs.harvard.edu/cgi-bin/nph-bib_query?bibcode='\n",
    "            end = '&data_type=BIBTEX&db_key=AST%26nocookieset=1'\n",
    "            url = uri + bibcode + end\n",
    "            bib = request.urlopen(url).read().decode('utf-8')\n",
    "            bib = bib.split('\\n')\n",
    "            self.bibtex = '\\n'.join(bib[5:-1])\n",
    "        finally:\n",
    "            return self.bibtex"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "@ARTICLE{2012PhRvA..85c2515Z,\n",
      "   author = {{Zhang}, S.~B. and {Yeager}, D.~L.},\n",
      "    title = \"{Complex-scaled multireference configuration-interaction method to study Be and Be-like cations' (B, C, N, O, Mg) Auger resonances 1s2s$^{2}$2p $^{1,3}$P$^{o}$}\",\n",
      "  journal = {\\pra},\n",
      " keywords = {Calculations and mathematical techniques in atomic and molecular physics, Other topics in the theory of the electronic structure of atoms and molecules, Auger effect and inner-shell excitation or ionization, Autoionization},\n",
      "     year = 2012,\n",
      "    month = mar,\n",
      "   volume = 85,\n",
      "   number = 3,\n",
      "      eid = {032515},\n",
      "    pages = {032515},\n",
      "      doi = {10.1103/PhysRevA.85.032515},\n",
      "   adsurl = {https://ui.adsabs.harvard.edu/abs/2012PhRvA..85c2515Z},\n",
      "  adsnote = {Provided by the SAO/NASA Astrophysics Data System}\n",
      "}\n",
      "\n"
     ]
    }
   ],
   "source": [
    "# Example\n",
    "doi = \"10.1103/PhysRevA.85.032515\"\n",
    "bib = Bibtex(doi)\n",
    "print(bib.getADS())\n",
    "\n",
    "# The first part after @ARTICLE is the Bibcode, in this case the Bibcode is '1998JMoSp.187...70B'"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\n",
      "ADS failed\n",
      "\n",
      "None\n"
     ]
    }
   ],
   "source": [
    "# Prompt!!!\n",
    "doi = \"ENTER DOI HERE\"\n",
    "bib = Bibtex(doi)\n",
    "print(bib.getADS())"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## <font color=green>Step 3. ADS Method</font>"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### <font color=green>Note before using ADS Method</font>\n",
    "  1. Exporting using bibcodes require two things.\n",
    "       - A Bibcode Number (which you got from step 2)<br>\n",
    "       - A Token--You will need to know what a Token is. It must be used whenever you want to access the ADS database. A token can only be used once you have an account on NASA/ADS https://ui.adsabs.harvard.edu/. Once you have an account click on 'Account' in the top right hand corner, then click on 'Customize Settings' on the dropdown menu. In 'Customize Settings' there is a panel to the left of the screen, if you scroll down that panel you will see 'API Token'. Click on 'API Token' and then click on 'generate a new key'. <br>\n",
    "         - You are technically using ADS's API when you are using this method. So for any questions/concerns please refer to the NASA/ADS API Information tool on GitHub https://github.com/adsabs/adsabs-dev-api#access-settings <br>\n",
    "  2. The benefits of this method are the endless choices to customize your citation output.\n",
    "     - You can get more information such as... the abstract, copyright, citation count, author affiliation, keywords, publication category and arXiv e-print number, etc.<br>\n",
    "     - You can search more than 1 bibcode at a time<br>\n",
    "     - You have more output options such as... EndNote, ProCite, RIS (Refman), RefWorks, MEDLARS, AASTeX, Icarus, MNRAS, Solar Physics (SoPh), DC (Dublin Core) XML, REF-XML, REFABS-XML, VOTables and RSS<br>\n",
    "     - This notebook does not display examples of all of these output format options, if you are interested in any of these choices or extra features please refer to http://adsabs.github.io/help/actions/export <br>\n",
    "  3. The first option is to retrieve a citation where the output is in JSON format<br>\n",
    "  4. The second option is to retrieve a citation where the output is in html format<br>\n",
    "  6. The third option is to retrieve a citation where the output is in LaTeX format</font>\n",
    "  \n",
    "*<font color=green>Overall you need to make an account on ADS in order to use this method. </font>*\n",
    "\n",
    "*<font color=green>If you do not want to make an account then use the BibTeX citation from step 6 and if you want, use steps 4 & 5 to retrieve html and JSON citation formats, in steps 4 & 5 you only need to enter the DOI to retrieve citations </font>*\n",
    "\n",
    "*<font color=green>However there are many benefits to using the ADS method, your citation output is completely customizable! So if your willing and you have your Bibcode then its recommended to use this method!</font>*"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### <font color=green>Below is an example on how to search using the ADS method and get a JSON output</font>"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "{'msg': 'Retrieved 1 abstracts, starting with number 1.', 'export': 'H2O-nu-0: Zhang, S. B. and D. L. Yeager, Title:Complex-scaled multireference configuration-interaction method to study Be and Be-like cations\\' (B, C, N, O, Mg) Auger resonances 1s2s<SUP>2</SUP>2p <SUP>1,3</SUP>P<SUP>o</SUP>, Physical Review A, 85, 032515, 2012, <a href=\"http://dx.doi.org\\\\10.1103/PhysRevA.85.032515\">DOI</a>}, <a href=\"https://ui.adsabs.harvard.edu/abs/2012PhRvA..85c2515Z\">Bibcode</a>'}\n"
     ]
    }
   ],
   "source": [
    "# Before each exporting option it should always start with 'import requests' and 'import json'\n",
    "\n",
    "import requests\n",
    "import json\n",
    "\n",
    "# This is where the token goes, between the \"\" \n",
    "token=\"gx43LyUuTTD0zoTWx8qKpWbWi3euTmx7FCM3fJjY\"\n",
    "\n",
    "# In the [] is where the bibcode(s) is/are entered, yes you can enter more than one bibcode at a time using this method\n",
    "# If you want to enter more than one bibcode just put a \\ inbetween them to seperate them\n",
    "payload = {\"bibcode\":[\"2012PhRvA..85c2515Z\"],\\\n",
    "           \"sort\": \"first_author asc\",\\\n",
    "          'format':\\\n",
    "           'H2O-nu-0: %I, Title:%T, %J, %V, %p-%P, %Y, <a href=\"http://dx.doi.org\\%d\">DOI</a>}, <a href=\"%u\">Bibcode</a>'}\n",
    "# Above in payload=, is the code for the format. I will explain what everything means in notes here.\n",
    "# At the beginning we give the reference an identifer, here thats H2O-nu-0\n",
    "# %I is a custom output for the authors, they generate the authors names as f. i. lastname with commas in between each author\n",
    "# %T gives the Title of the article\n",
    "# %J this gives the journal name \n",
    "# %V this gives the volume number for the article \n",
    "# %p-%P this gives the first page to the last page for the article\n",
    "# %Y this gives the year of the article\n",
    "# hyperlinks only work with the format <a href=\"ENTER HYPERLINK HERE\">LINK IDENTIFIER</a>\n",
    "# %d in the first hyperlink grabs the DOI for the article, \n",
    "# therefore this is in the hyperlink portion so the output is https://doi.org/doi_number (labeled as DOI)\n",
    "# %u in the second hyperlink, it grabs the bibcode only(%u), no need to add an https portion, then the identifer is Bibcode\n",
    "\n",
    "r = requests.post(\"https://api.adsabs.harvard.edu/v1/export/custom\", \\\n",
    "                 headers={\"Authorization\": \"Bearer \" + token, \"Content-type\": \"application/json\"}, \\\n",
    "                 data=json.dumps(payload))\n",
    "# above we are requesting ads for permission to access this information, then we ask it to provide an output for our reference\n",
    "\n",
    "# below we print the reference in json format\n",
    "print(r.json())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "{'error': 'Unauthorized'}\n"
     ]
    }
   ],
   "source": [
    "# This is a prompt to search using the ADS method and retrieve a JSON output\n",
    "\n",
    "import requests\n",
    "import json\n",
    "\n",
    "token=\"ENTER TOKEN HERE\"\n",
    "\n",
    "payload = {\"bibcode\":[\"ENTER BIBCODE HERE\"],\\\n",
    "           \"sort\": \"first_author asc\",\\\n",
    "          'format':\\\n",
    "           'ENTER NOTES OR LABELS HERE: %I, \"%T\", <i>%J</i>, <b>%V</b>, %p-%P, (%Y), <a href=\"https:\\\\doi.org\\%d\">DOI</a>, <a href=\"%u\">Bibcode</a>'}\n",
    "r = requests.post(\"https://api.adsabs.harvard.edu/v1/export/custom\", \\\n",
    "                 headers={\"Authorization\": \"Bearer \" + token, \"Content-type\": \"application/json\"}, \\\n",
    "                 data=json.dumps(payload))\n",
    "print(r.json())"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### <font color=green>Below is an example on how to search using the ADS method and get an HTML output</font>"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "{'msg': 'Retrieved 1 abstracts, starting with number 1.', 'export': '<p> Note: H2O-nu-0, Kurtz, M. J., G. Eichhorn, A. Accomazzi, C. S. Grant, S. S. Murray, and J. M. Watson, \"The NASA Astrophysics Data System: Overview\", <i>Astronomy and Astrophysics Supplement Series</i>, <b>143</b>, 41-59, (2000), <a href=\"https:\\\\doi.org\\\\10.1051/aas:2000170\">DOI</a>, <a href=\"https://ui.adsabs.harvard.edu/abs/2000A&amp;AS..143...41K\">Bibcode</a>'}\n"
     ]
    }
   ],
   "source": [
    "# This is an example of using the ADS method to retrieve a citation in HTML format\n",
    "# I provided this as a second option, it is exactly the same as the one above, except there is an %Encoding:html<p> portion\n",
    "# this portion converts characters in URLs to hex notation. Outside URLs, the characters “ and \" are converted respectively.\n",
    "# in simple terms this helps encode the output to be html formatted\n",
    "\n",
    "import requests\n",
    "import json\n",
    "\n",
    "token=\"gx43LyUuTTD0zoTWx8qKpWbWi3euTmx7FCM3fJjY\"\n",
    "payload = {\"bibcode\":[\"2000A&AS..143...41K\"],\\\n",
    "          \"sort\": \"first_author asc\",\\\n",
    "          'format': '%ZEncoding:html<p> Note: H2O-nu-0, %I, \"%T\", <i>%J</i>, <b>%V</b>, %p-%P, (%Y), <a href=\"https:\\\\doi.org\\%d\">DOI</a>, <a href=\"%u\">Bibcode</a>'}\n",
    "r = requests.post(\"https://api.adsabs.harvard.edu/v1/export/custom\", \\\n",
    "                 headers={\"Authorization\": \"Bearer \" + token, \"Content-type\": \"application/json\"}, \\\n",
    "                 data=json.dumps(payload))\n",
    "print(r.json())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "{'error': 'Unauthorized'}\n"
     ]
    }
   ],
   "source": [
    "# This is a prompt using the ADS method to retrieve a citation in HTML format\n",
    "\n",
    "import requests\n",
    "import json\n",
    "\n",
    "token=\"ENTER TOKEN HERE\"\n",
    "payload = {\"bibcode\":[\"ENTER BIBCODE HERE\"],\\\n",
    "          \"sort\": \"first_author asc\",\\\n",
    "          'format': '%ZEncoding:html<p> :ENTER NOTES OR LABELS HERE, %I, \"%T\", <i>%J</i>, <b>%V</b>, %p-%P, (%Y), <a href=\"https:\\\\doi.org\\%d\">DOI</a>, <a href=\"%u\">Bibcode</a>'}\n",
    "r = requests.post(\"https://api.adsabs.harvard.edu/v1/export/custom\", \\\n",
    "                 headers={\"Authorization\": \"Bearer \" + token, \"Content-type\": \"application/json\"}, \\\n",
    "                 data=json.dumps(payload))\n",
    "print(r.json())"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### <font color=green>Below is an example on how to search using the ADS method and get a LaTeX output</font>"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "{'msg': 'Retrieved 1 abstracts, starting with number 1.', 'export': '\\\\bibitem[Note: H2O-nu-0, Kurtz, M.~J., G. Eichhorn, A. Accomazzi, C.~S. Grant, S.~S. Murray, and J.~M. Watson, \"The NASA Astrophysics Data System: Overview\", \\textit{Astronomy and Astrophysics Supplement Series}, \\textbf{143}, 41-59, (2000), {10.1051/aas:2000170}, {https://ui.adsabs.harvard.edu/abs/2000A\\\\&AS..143...41K}:]'}\n"
     ]
    }
   ],
   "source": [
    "# I provided this as a third option, it is exactly the same as the first except there is a %Encoding:latex\\\\item portion \n",
    "# The %Encoding:latex converts all special Tex characters into their Tex escape sequences\n",
    "# For instance ‘\\’ is converted to ‘$\\backslash $’, ‘$’ is converted into ‘\\$’, ‘^’ is converted into ‘\\^{}’, etc.\n",
    "# The format is also latex encoded too, the first change starts with \\textit{%J} which italisizes the journal name\n",
    "# \\textbf{%V} bolds the volume number\n",
    "    \n",
    "import requests\n",
    "import json\n",
    "\n",
    "token=\"gx43LyUuTTD0zoTWx8qKpWbWi3euTmx7FCM3fJjY\"\n",
    "payload = {\"bibcode\":[\"2000A&AS..143...41K\"],\\\n",
    "          \"sort\": \"first_author asc\",\\\n",
    "          'format': '%ZEncoding:latex\\\\bibitem[Note: H2O-nu-0, %I, \"%T\", \\textit{%J}, \\textbf{%V}, %p-%P, (%Y), {%d}, {%u}:]'}\n",
    "r = requests.post(\"https://api.adsabs.harvard.edu/v1/export/custom\", \\\n",
    "                 headers={\"Authorization\": \"Bearer \" + token, \"Content-type\": \"application/json\"}, \\\n",
    "                 data=json.dumps(payload))\n",
    "print(r.json())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "{'error': 'Unauthorized'}\n"
     ]
    }
   ],
   "source": [
    "# This is a prompt using the ADS method to retrieve a citation in LaTeX format\n",
    "\n",
    "import requests\n",
    "import json\n",
    "\n",
    "token=\"ENTER TOKEN HERE\"\n",
    "payload = {\"bibcode\":[\"ENTER BIBCODE HERE\"],\\\n",
    "          \"sort\": \"first_author asc\",\\\n",
    "          'format': '%ZEncoding:latex\\\\bibitem[Note: ENTER NOTE OR LABEL HERE, %I, \"%T\", \\textit{%J}, \\textbf{%V}, %p-%P, (%Y), {%d}, {%u}:]'}\n",
    "r = requests.post(\"https://api.adsabs.harvard.edu/v1/export/custom\", \\\n",
    "                 headers={\"Authorization\": \"Bearer \" + token, \"Content-type\": \"application/json\"}, \\\n",
    "                 data=json.dumps(payload))\n",
    "print(r.json())"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## <font color=purple>Step 4. Urllib method</font> "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "# This is the code to retrieve the citation. \n",
    "# Below this cell is an example of retrieving the citation using an example DOI and a Prompt to Enter your DOI!\n",
    "\n",
    "import json\n",
    "import urllib.request\n",
    "from urllib.error import HTTPError\n",
    "\n",
    "def get_citeproc_authors(cpd_author):\n",
    "    if cpd_author is None:\n",
    "        return None\n",
    "    names = []\n",
    "    for author in cpd_author:\n",
    "        try:\n",
    "            family = author['family'].title()\n",
    "        except KeyError:\n",
    "            # Occasionally an author isn't a single person,\n",
    "            # e.g. \"JET contributors\", so do what we can here:\n",
    "            name = author['name']\n",
    "            names.append(name)\n",
    "            continue\n",
    "        try:\n",
    "            given = author['given']\n",
    "        except KeyError:\n",
    "            # This author has a first name\n",
    "            names.append(family)\n",
    "            continue\n",
    "        initials = given.split()\n",
    "        initials[0] = '{}.'.format(initials[0][0])\n",
    "        initials = ' '.join(initials)\n",
    "        names.append('{} {}'.format(initials, family))\n",
    "    return ', '.join(names)\n",
    "\n",
    "def parse_citeproc_json(citeproc_json):\n",
    "    \"\"\"Parse the provided JSON into a Ref object.\"\"\"\n",
    "\n",
    "    cpd = json.loads(citeproc_json)\n",
    "    try:\n",
    "        if cpd['type'] != 'article-journal':\n",
    "            return None\n",
    "    except KeyError:\n",
    "        return None\n",
    "\n",
    "    authors = get_citeproc_authors(cpd.get('author', ''))\n",
    "    title = cpd.get('title', '').replace('\\n', '')\n",
    "    journal = cpd.get('container-title', '')\n",
    "    volume = cpd.get('volume', '')\n",
    "    page_start, page_end = cpd.get('page', ''), ''\n",
    "    if page_start and '-' in page_start:\n",
    "        page_start, page_end = page_start.split('-')\n",
    "    article_number = cpd.get('article-number', '')\n",
    "    doi = cpd.get('DOI', '')\n",
    "    url = cpd.get('URL', '')\n",
    "    try:\n",
    "        year = cpd['issued']['date-parts'][0][0]\n",
    "    except (KeyError, IndexError):\n",
    "        year = None\n",
    "# # =============================================================================\n",
    "# #   OUTPUT\n",
    "# # =============================================================================\n",
    "    ref = [authors, \n",
    "        title, \n",
    "        journal, \n",
    "        volume,\n",
    "        year, \n",
    "        page_start, \n",
    "        page_end, \n",
    "        doi,\n",
    "        url, \n",
    "        article_number,\n",
    "        citeproc_json]\n",
    "\n",
    "    # ref = Ref(authors=authors, title=title, journal=journal, volume=volume,\n",
    "              # year=year, page_start=page_start, page_end=page_end, doi=doi,\n",
    "              # url=url, article_number=article_number,\n",
    "              # citeproc_json=citeproc_json)\n",
    "    return ref \n",
    "\n",
    "def get_citeproc_json_from_doi(doi):\n",
    "    base_url = 'http://dx.doi.org/'\n",
    "    url = base_url + doi\n",
    "    req = urllib.request.Request(url)\n",
    "    req.add_header('Accept', 'application/citeproc+json')\n",
    "    try:\n",
    "        with urllib.request.urlopen(req) as f:\n",
    "            citeproc_json = f.read().decode()\n",
    "    except HTTPError as e:\n",
    "        if e.code == 404:\n",
    "            raise ValueError('DOI not found.')\n",
    "        raise\n",
    "    return citeproc_json\n",
    "\n",
    "def get_source_from_doi(doi):\n",
    "    citeproc_json = get_citeproc_json_from_doi(doi)\n",
    "    ref = parse_citeproc_json(citeproc_json)\n",
    "    return ref"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "S. Bin Zhang, D. L. Yeager ; Complex-scaled multireference configuration-interaction method to study Be and Be-like cations' (B, C, N, O, Mg) Auger resonances1s2s22p1,3Po ; Physical Review A ; 85 ; 2012 ; p.  -  ; 10.1103/physreva.85.032515 ; http://dx.doi.org/10.1103/PhysRevA.85.032515\n"
     ]
    }
   ],
   "source": [
    "# Example\n",
    "\n",
    "doi_fetched = get_source_from_doi('10.1103/PhysRevA.85.032515')\n",
    "\n",
    "print (doi_fetched[0],';',doi_fetched[1],';',doi_fetched[2],';',doi_fetched[3],';',doi_fetched[4],'; p.',doi_fetched[5],'-',doi_fetched[6],';',doi_fetched[7],';', doi_fetched[8])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {
    "collapsed": true
   },
   "outputs": [
    {
     "ename": "HTTPError",
     "evalue": "HTTP Error 400: Bad Request",
     "output_type": "error",
     "traceback": [
      "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[1;31mHTTPError\u001b[0m                                 Traceback (most recent call last)",
      "\u001b[1;32m<ipython-input-12-4f984fc7b31c>\u001b[0m in \u001b[0;36m<module>\u001b[1;34m\u001b[0m\n\u001b[1;32m----> 1\u001b[1;33m \u001b[0mdoi_fetched\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mget_source_from_doi\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;34m'ENTER DOI HERE'\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m      2\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m      3\u001b[0m \u001b[1;31m# Below are the parameters for searching your citation, if you would like to add or change anything then refer to the initial code above to make your changes\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m      4\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m      5\u001b[0m \u001b[0mprint\u001b[0m \u001b[1;33m(\u001b[0m\u001b[1;34m'Authors:'\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mdoi_fetched\u001b[0m\u001b[1;33m[\u001b[0m\u001b[1;36m0\u001b[0m\u001b[1;33m]\u001b[0m\u001b[1;33m,\u001b[0m \u001b[1;34m''\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;32m<ipython-input-10-3d213911f799>\u001b[0m in \u001b[0;36mget_source_from_doi\u001b[1;34m(doi)\u001b[0m\n\u001b[0;32m     91\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m     92\u001b[0m \u001b[1;32mdef\u001b[0m \u001b[0mget_source_from_doi\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mdoi\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m---> 93\u001b[1;33m     \u001b[0mciteproc_json\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mget_citeproc_json_from_doi\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mdoi\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m     94\u001b[0m     \u001b[0mref\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mparse_citeproc_json\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mciteproc_json\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m     95\u001b[0m     \u001b[1;32mreturn\u001b[0m \u001b[0mref\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;32m<ipython-input-10-3d213911f799>\u001b[0m in \u001b[0;36mget_citeproc_json_from_doi\u001b[1;34m(doi)\u001b[0m\n\u001b[0;32m     82\u001b[0m     \u001b[0mreq\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0madd_header\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;34m'Accept'\u001b[0m\u001b[1;33m,\u001b[0m \u001b[1;34m'application/citeproc+json'\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m     83\u001b[0m     \u001b[1;32mtry\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m---> 84\u001b[1;33m         \u001b[1;32mwith\u001b[0m \u001b[0murllib\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mrequest\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0murlopen\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mreq\u001b[0m\u001b[1;33m)\u001b[0m \u001b[1;32mas\u001b[0m \u001b[0mf\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m     85\u001b[0m             \u001b[0mciteproc_json\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mf\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mread\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mdecode\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m     86\u001b[0m     \u001b[1;32mexcept\u001b[0m \u001b[0mHTTPError\u001b[0m \u001b[1;32mas\u001b[0m \u001b[0me\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;32m~\\AppData\\Local\\Continuum\\anaconda3\\lib\\urllib\\request.py\u001b[0m in \u001b[0;36murlopen\u001b[1;34m(url, data, timeout, cafile, capath, cadefault, context)\u001b[0m\n\u001b[0;32m    220\u001b[0m     \u001b[1;32melse\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    221\u001b[0m         \u001b[0mopener\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0m_opener\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m--> 222\u001b[1;33m     \u001b[1;32mreturn\u001b[0m \u001b[0mopener\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mopen\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0murl\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mdata\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mtimeout\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m    223\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    224\u001b[0m \u001b[1;32mdef\u001b[0m \u001b[0minstall_opener\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mopener\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;32m~\\AppData\\Local\\Continuum\\anaconda3\\lib\\urllib\\request.py\u001b[0m in \u001b[0;36mopen\u001b[1;34m(self, fullurl, data, timeout)\u001b[0m\n\u001b[0;32m    529\u001b[0m         \u001b[1;32mfor\u001b[0m \u001b[0mprocessor\u001b[0m \u001b[1;32min\u001b[0m \u001b[0mself\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mprocess_response\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mget\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mprotocol\u001b[0m\u001b[1;33m,\u001b[0m \u001b[1;33m[\u001b[0m\u001b[1;33m]\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    530\u001b[0m             \u001b[0mmeth\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mgetattr\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mprocessor\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mmeth_name\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m--> 531\u001b[1;33m             \u001b[0mresponse\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mmeth\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mreq\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mresponse\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m    532\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    533\u001b[0m         \u001b[1;32mreturn\u001b[0m \u001b[0mresponse\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;32m~\\AppData\\Local\\Continuum\\anaconda3\\lib\\urllib\\request.py\u001b[0m in \u001b[0;36mhttp_response\u001b[1;34m(self, request, response)\u001b[0m\n\u001b[0;32m    639\u001b[0m         \u001b[1;32mif\u001b[0m \u001b[1;32mnot\u001b[0m \u001b[1;33m(\u001b[0m\u001b[1;36m200\u001b[0m \u001b[1;33m<=\u001b[0m \u001b[0mcode\u001b[0m \u001b[1;33m<\u001b[0m \u001b[1;36m300\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    640\u001b[0m             response = self.parent.error(\n\u001b[1;32m--> 641\u001b[1;33m                 'http', request, response, code, msg, hdrs)\n\u001b[0m\u001b[0;32m    642\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    643\u001b[0m         \u001b[1;32mreturn\u001b[0m \u001b[0mresponse\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;32m~\\AppData\\Local\\Continuum\\anaconda3\\lib\\urllib\\request.py\u001b[0m in \u001b[0;36merror\u001b[1;34m(self, proto, *args)\u001b[0m\n\u001b[0;32m    567\u001b[0m         \u001b[1;32mif\u001b[0m \u001b[0mhttp_err\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    568\u001b[0m             \u001b[0margs\u001b[0m \u001b[1;33m=\u001b[0m \u001b[1;33m(\u001b[0m\u001b[0mdict\u001b[0m\u001b[1;33m,\u001b[0m \u001b[1;34m'default'\u001b[0m\u001b[1;33m,\u001b[0m \u001b[1;34m'http_error_default'\u001b[0m\u001b[1;33m)\u001b[0m \u001b[1;33m+\u001b[0m \u001b[0morig_args\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m--> 569\u001b[1;33m             \u001b[1;32mreturn\u001b[0m \u001b[0mself\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0m_call_chain\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;33m*\u001b[0m\u001b[0margs\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m    570\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    571\u001b[0m \u001b[1;31m# XXX probably also want an abstract factory that knows when it makes\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;32m~\\AppData\\Local\\Continuum\\anaconda3\\lib\\urllib\\request.py\u001b[0m in \u001b[0;36m_call_chain\u001b[1;34m(self, chain, kind, meth_name, *args)\u001b[0m\n\u001b[0;32m    501\u001b[0m         \u001b[1;32mfor\u001b[0m \u001b[0mhandler\u001b[0m \u001b[1;32min\u001b[0m \u001b[0mhandlers\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    502\u001b[0m             \u001b[0mfunc\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mgetattr\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mhandler\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mmeth_name\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m--> 503\u001b[1;33m             \u001b[0mresult\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mfunc\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;33m*\u001b[0m\u001b[0margs\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m    504\u001b[0m             \u001b[1;32mif\u001b[0m \u001b[0mresult\u001b[0m \u001b[1;32mis\u001b[0m \u001b[1;32mnot\u001b[0m \u001b[1;32mNone\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    505\u001b[0m                 \u001b[1;32mreturn\u001b[0m \u001b[0mresult\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;32m~\\AppData\\Local\\Continuum\\anaconda3\\lib\\urllib\\request.py\u001b[0m in \u001b[0;36mhttp_error_default\u001b[1;34m(self, req, fp, code, msg, hdrs)\u001b[0m\n\u001b[0;32m    647\u001b[0m \u001b[1;32mclass\u001b[0m \u001b[0mHTTPDefaultErrorHandler\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mBaseHandler\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    648\u001b[0m     \u001b[1;32mdef\u001b[0m \u001b[0mhttp_error_default\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mself\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mreq\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mfp\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mcode\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mmsg\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mhdrs\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m--> 649\u001b[1;33m         \u001b[1;32mraise\u001b[0m \u001b[0mHTTPError\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mreq\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mfull_url\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mcode\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mmsg\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mhdrs\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mfp\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m    650\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    651\u001b[0m \u001b[1;32mclass\u001b[0m \u001b[0mHTTPRedirectHandler\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mBaseHandler\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;31mHTTPError\u001b[0m: HTTP Error 400: Bad Request"
     ]
    }
   ],
   "source": [
    "# Prompt\n",
    "\n",
    "doi_fetched = get_source_from_doi('ENTER DOI HERE')\n",
    "\n",
    "# Below are the parameters for searching your citation, if you would like to add or change anything then refer to the initial code above to make your changes\n",
    "\n",
    "print ('Authors:', doi_fetched[0], '')\n",
    "print ('Title:', doi_fetched[1], '')\n",
    "print ('Journal:', doi_fetched[2], '')\n",
    "print ('Volume:', doi_fetched[3], '')\n",
    "print ('Year:', doi_fetched[4], '')\n",
    "print ('Page Start:', doi_fetched[5], '')\n",
    "print ('Page End:', doi_fetched[6], '')\n",
    "print ('DOI:', doi_fetched[7], '')\n",
    "print ('URL:', doi_fetched[8], '')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## <font color=teal>Step 5. Encoding JSON in HTML</font> <br>"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "'C. J. Young, M. D. Hurley, T. J. Wallington, S. A. Mabury ; Atmospheric chemistry of perfluorobutenes (CF3CFCFCF3 and CF3CF2CFCF2): Kinetics and mechanisms of reactions with OH radicals and chlorine atoms, IR spectra, global warming potentials, and oxidation to perfluorocarboxylic acids ; Atmospheric Environment ; 43 ; 2009 ; p. 3717 - 3724 ; 10.1016/j.atmosenv.2009.04.025 ; http://dx.doi.org/10.1016/j.atmosenv.2009.04.025&#x27;'"
      ]
     },
     "execution_count": 13,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Note: Use the JSON output from urllib\n",
    "# Example of encoding the JSON output from Urllib\n",
    "\n",
    "from html.entities import html5 as _html5\n",
    "import html\n",
    "\n",
    "s = html.escape( \"\"\"& < \" ' >\"\"\" )   # s = '&amp; &lt; &quot; &#x27; &gt;'\n",
    "html.escape(s, quote=True)\n",
    "html.escape(\"C. J. Young, M. D. Hurley, T. J. Wallington, S. A. Mabury ; Atmospheric chemistry of perfluorobutenes (CF3CFCFCF3 and CF3CF2CFCF2): Kinetics and mechanisms of reactions with OH radicals and chlorine atoms, IR spectra, global warming potentials, and oxidation to perfluorocarboxylic acids ; Atmospheric Environment ; 43 ; 2009 ; p. 3717 - 3724 ; 10.1016/j.atmosenv.2009.04.025 ; http://dx.doi.org/10.1016/j.atmosenv.2009.04.025'\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "'{&#x27;msg&#x27;: &#x27;Retrieved 1 abstracts, starting with number 1.&#x27;, &#x27;export&#x27;: &#x27;H2O-nu-0: Kurtz, M. J., G. Eichhorn, A. Accomazzi, C. S. Grant, S. S. Murray, and J. M. Watson, Title:The NASA Astrophysics Data System: Overview, Astronomy and Astrophysics Supplement Series, 143, 41-59, 2000, dx.doi.org\\\\10.1051/aas:2000170, https://ui.adsabs.harvard.edu/abs/2000A&amp;AS..143...41K&#x27;}'"
      ]
     },
     "execution_count": 14,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Encoding the JSON output from ADS \n",
    "\n",
    "# Note:\"<a href=\"http://dx.doi.org\\\\10.1051/aas:2000170\">DOI</a>}, <a href=\"https://ui.adsabs.harvard.edu/abs/2000A&AS..143...41K\">Bibcode</a>'\"\n",
    "# These above url formats produced by ADS will not code correctly and you will receive an error, to fix this change them to...\n",
    "# dx.doi.org\\\\10.1051/aas:2000170, https://ui.adsabs.harvard.edu/abs/2000A&AS..143...41K\n",
    "\n",
    "from html.entities import html5 as _html5\n",
    "import html\n",
    "\n",
    "s = html.escape( \"\"\"& < \" ' >\"\"\" )   # s = '&amp; &lt; &quot; &#x27; &gt;'\n",
    "html.escape(s, quote=True)\n",
    "html.escape(\"{'msg': 'Retrieved 1 abstracts, starting with number 1.', 'export': 'H2O-nu-0: Kurtz, M. J., G. Eichhorn, A. Accomazzi, C. S. Grant, S. S. Murray, and J. M. Watson, Title:The NASA Astrophysics Data System: Overview, Astronomy and Astrophysics Supplement Series, 143, 41-59, 2000, dx.doi.org\\\\10.1051/aas:2000170, https://ui.adsabs.harvard.edu/abs/2000A&AS..143...41K'}\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "'ENTER JSON OUTPUT HERE'"
      ]
     },
     "execution_count": 15,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Prompt\n",
    "\n",
    "from html.entities import html5 as _html5\n",
    "import html\n",
    "\n",
    "s = html.escape( \"\"\"& < \" ' >\"\"\" )   # s = '&amp; &lt; &quot; &#x27; &gt;'\n",
    "html.escape(s, quote=True)\n",
    "html.escape(\"ENTER JSON OUTPUT HERE\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## <font color=maroon>Step 6. BibTeX citation</font>"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {},
   "outputs": [],
   "source": [
    "# If you have not already recieved the BibTeX citation then it is because your paper is not in ADS\n",
    "# Step 1 and 3 both have can give you BibTeX citations but they require that your paper is in ADS\n",
    "# This method only uses GScholar and does not utilize ADS, therefore you can retrieve your BibTeX citation here \n",
    "# This is the code to retrieve the citation. \n",
    "# Below this cell is an example of retrieving the citation using an example DOI and a Prompt to Enter your DOI!\n",
    "\n",
    "import gscholar  \n",
    "import urllib\n",
    "import bs4\n",
    "from gscholar import query\n",
    "from urllib import request, parse\n",
    "from bs4 import BeautifulSoup \n",
    "\n",
    "#Class Bibtex\n",
    "class Bibtex(object):\n",
    "    \"\"\" Convert doi number to get bibtex entries.\"\"\"\n",
    "    def __init__(self, doi=None, title=None):\n",
    "        \"\"\"Input doi number-- Returns doi, encoded doi, and doi url.\"\"\"\n",
    "        _base_url = \"http://dx.doi.org/\"\n",
    "        self.doi = doi\n",
    "        self.title = title\n",
    "        self.bibtex = None\n",
    "        if doi:\n",
    "            self._edoi = parse.quote(doi)\n",
    "            self.url = _base_url + self._edoi  #Encoded doi.\n",
    "        else:\n",
    "            self.url = None    \n",
    "\n",
    "#Beautiful Soup is a Python library for pulling data out of HTML and XML files\n",
    "    def _soupfy(self, url):\n",
    "        \"\"\"Returns a soup object.\"\"\"\n",
    "        html = request.urlopen(url).read()\n",
    "        self.soup = BeautifulSoup(html)\n",
    "        return self.soup                \n",
    "\n",
    "    def getGScholar(self):\n",
    "        bibtex = query(self.doi, 4)[0]\n",
    "        self.bibtex = bibtex\n",
    "        return self.bibtex"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "@article{biennier1998high,\n",
      "  title={High Resolution Spectrum of the (3--0) Band of theb1$\\Sigma$+ g--X3$\\Sigma$- gRed Atmospheric System of Oxygen},\n",
      "  author={Biennier, Ludovic and Campargue, Alain},\n",
      "  journal={Journal of molecular spectroscopy},\n",
      "  volume={2},\n",
      "  number={188},\n",
      "  pages={248--250},\n",
      "  year={1998}\n",
      "}\n",
      "\n"
     ]
    }
   ],
   "source": [
    "# Example\n",
    "doi = \"10.1006/jmsp.1997.7521\"\n",
    "bib = Bibtex(doi)\n",
    "print(bib.getGScholar())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "@article{prashant2009managing,\n",
      "  title={Managing strategic alliances: what do we know now, and where do we go from here?},\n",
      "  author={Prashant, Kale and Harbir, Singh},\n",
      "  journal={Academy of management perspectives},\n",
      "  volume={23},\n",
      "  number={3},\n",
      "  pages={45--62},\n",
      "  year={2009},\n",
      "  publisher={Academy of Management Briarcliff Manor, NY}\n",
      "}\n",
      "\n"
     ]
    }
   ],
   "source": [
    "# Prompt\n",
    "# Note this method can either search for DOI, Keywords or Titles\n",
    "doi = \"ENTER DOI HERE\"\n",
    "bib = Bibtex(doi)\n",
    "print(bib.getGScholar())"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
