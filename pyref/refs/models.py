from django.db import models
import json
import urllib.request
from urllib.error import HTTPError
from .utils import ensure_https

class Ref(models.Model):
    """A literature reference, for example a journal article, book etc."""

    # A list of the authors' names in a string as:
    # 'A. N. Other, B.-C. Person Jr., Ch. Someone-Someone, N. M. L. Haw Haw'
    # DO NOT separate names with "AND" (even before the last author).
    authors = models.TextField(blank=True,
        help_text='Comma-delimited names with space-separated initials first'
                  ' (no ANDs). e.g. "A. N. Other, B.-C. Person Jr., Ch. '
                  'Someone-Someone, N. M. L. Haw Haw"')

    # The article, book, or thesis title.
    title = models.TextField(blank=True,
        help_text='Best-effort UTF-8 encoded plaintext version of title. No'
                  ' HTML tags, markdown or LaTeX.')
    # The title as HTML.
    title_html = models.TextField(blank=True,
        help_text="Valid HTML version of title. Don't wrap with &lt;p&gt; or"
                  " other tags.")
    # The title as LaTeX.
    title_latex = models.TextField(blank=True,
        help_text="LaTeX version of title. Don't escape backslashes (\\) but"
                  " do use valid LaTeX for accented and similar characers.")

    # The journal name.
    journal = models.CharField(max_length=500, blank=True)
    # The volume (which may be a string).
    volume = models.CharField(max_length=10, blank=True)
    # The first page (which may be a string e.g. 'L123').
    page_start = models.CharField(max_length=10, blank=True)
    # The last page
    page_end = models.CharField(max_length=10, blank=True)
    # Article number, used instead of page number by some journals (e.g.
    # J. Chem. Phys.)
    article_number = models.CharField(max_length=16, blank=True)

    # The publication year (as an integer, YYYY).
    year = models.IntegerField(null=True, blank=True)

    # For flexibility, allow free-form "notes" as references, e.g.
    # private communications, comments, etc.
    note = models.TextField(blank=True)
    # the note as HTML
    note_html = models.TextField(blank=True)
    # the note as LaTeX
    note_latex = models.TextField(blank=True)

    # the Digital Object Identifier, if available.
    doi = models.CharField(max_length=100, blank=True)
    # a URL to the source, if available; if not provided the model will
    # construct https://dx.doi.org/<DOI>
    url = models.URLField(blank=True,
        help_text="If not provided, this will be automatically constructed"
                  " as https://dx.doi.org/&lt;DOI&gt; if possible.")

    # BibTeX entry as a string.
    bibtex = models.TextField(null=True, blank=True)
    # Research Information Systems (RIS) standardized tag formatted string.
    ris = models.TextField(null=True, blank=True)
    # JSON text string in CiteProc format.
    citeproc_json = models.TextField(null=True, blank=True)

    def _get_or_missing(self, field_name):
        """Try to get the value of field_name or say it's missing."""

        s = getattr(self, field_name)
        if not s:
            return '[missing {}]'.format(field_name)
        return s

    def __str__(self):
        """Simple string representation of the reference."""

        return '{}: {}, {}'.format(self.id, self._get_or_missing('authors'),
                                   self._get_or_missing('title'))

    @property
    def qualified_id(self):
        """Return the Ref's Primary Key ID as a string, prefixed with 'B'."""
        return 'B{}'.format(self.id)

    def _make_url_html(self, s_url=None):
        """Try to make an HTML <a> tag for the reference's URL."""

        if s_url is None:
            s_url = self.url
        if s_url:
            return '<span class="noprint"> [<a href="{}">link to article'\
                    '</a>]</span>'.format(s_url)
        return ''

    def _make_url_html_from_doi(self):
        """Try to make an HTML <a> tag from the reference's DOI."""

        if self.doi:
            s_url = 'https://dx.doi.org/{}'.format(self.doi)
            return self._make_url_html(s_url)
        return ''

    def shorten_authors(self, nmax=5, nret=1):
        """
        Return a shortened list of authors, limited to nret names plus "et al."
        if there are more than nmax authors associated with a Ref object.

        If nmax is None, then return all author names.

        """

        if nmax == None:
            return self.authors

        if not self.authors:
            return ''
        authors = self.authors.split(',')
        nauthors = len(authors)

        if nauthors == 1:
            return self.authors

        if nauthors > nmax:
            return ', '.join(authors[:nret]) + ' et al.'

        return ', '.join(authors[:nauthors-1]) + ' and ' + authors[-1]

    def parse_authors(self):
        """Parse the authors string to a list of (initials, surname) tuples."""

        s_authors = self.authors.split(',')
        l_authors = []
        for author in s_authors:
            initials = []
            fragments = author.split()
            for i, s in enumerate(fragments):
                if s[-1] == '.':
                    initials.append(s.strip())
                else:
                   break
            surname = ' '.join(fragments[i:])
            l_authors.append( (initials, surname) )
        return l_authors

    def _get_html_title(self):
        """Return the HTML title, if possible; otherwise use plain text."""

        return self.title_html or self._get_or_missing('title')

    def html_article(self, pk=True, authors_nmax=None):
        """Return the HTML markup for the Ref."""

        s_pk = ''
        if pk:
            s_pk = 'B{}: '.format(self.pk)
        s_authors = self.shorten_authors(nmax=authors_nmax)
        if s_authors:
            s_authors += ', '
        s_title = '"{}"'.format(self._get_html_title())
        s_journal = '<em>{}</em>'.format(self._get_or_missing('journal'))
        s_volume = ' <b>{}</b>'.format(self.volume) if self.volume else ''
        s_pages = ' '
        if self.page_start:
            if self.page_end:
                s_pages = ', {}-{}'.format(self.page_start, self.page_end)
            else:
                s_pages = ', {}'.format(self.page_start)

        s_article_number = ' '
        if self.article_number:
            s_article_number = ', {} '.format(self.article_number)
            s_pages = ''
        elif s_pages != ' ':
            s_article_number = ''

        s_year = '({})'.format(self.year) if self.year else ''
        s_url = self._make_url_html() or self._make_url_html_from_doi()

        s = '{s_pk}{authors}{title}, {journal}{volume}{pages}'\
            '{article_number} {year}. {url}'.format(s_pk=s_pk,
            authors=s_authors, title=s_title, journal=s_journal,
            volume=s_volume, pages=s_pages, article_number=s_article_number,
            year=s_year, url=s_url)
        return s

    def html(self, *args, **kwargs):
        """Return the HTML markup for the Ref."""

        return self.html_article(*args, **kwargs)

# Here are some utility functions for obtaining Ref objects from external
# sources and parsing different bibliographic formats.

def get_citeproc_authors(cpd_author):
    if cpd_author is None:
        return None
    names = []
    for author in cpd_author:
        try:
            family = author['family'].title()
        except KeyError:
            # Occasionally an author isn't a single person,
            # e.g. "JET contributors", so do what we can here:
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

def parse_citeproc_json(citeproc_json, ref=None):
    """Parse the provided JSON into a Ref object."""

    cpd = json.loads(citeproc_json)
    # We only understand journal articles, for now.
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
    url = ensure_https(cpd.get('URL', ''))
    try:
        year = cpd['issued']['date-parts'][0][0]
    except (KeyError, IndexError):
        year = None

    if ref:
        ref.authors = authors
        ref.title = title
        ref.journal = journal
        ref.volume = volume
        ref.year = year
        ref.page_start = page_start
        ref.page_end = page_end
        ref.doi = doi
        ref.url = url
        ref.article_number = article_number
        ref.citeproc_json = citeproc_json
    else:
        ref = Ref(authors=authors, title=title, journal=journal, volume=volume,
                  year=year, page_start=page_start, page_end=page_end, doi=doi,
                  url=url, article_number=article_number,
                  citeproc_json=citeproc_json)
    return ref 

def get_citeproc_json_from_doi(doi):
    base_url = 'https://doi.org/'
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

def get_ref_from_doi(doi, ref=None):
    citeproc_json = get_citeproc_json_from_doi(doi)
    ref = parse_citeproc_json(citeproc_json, ref)
    return ref

