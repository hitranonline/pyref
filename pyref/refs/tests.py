from django.test import TestCase


class DOIResolveTest(TestCase):

    def test_resolving_doi_populates_add_reference_page(self):
        doi = '10.1103/PhysRevA.85.032515'
        url = '/refs/resolve/?doi=' + doi
        response = self.client.get(url)
        
        self.assertContains(response,
    r'<input type="text" name="journal" value="Physical Review A" maxlength="500" id="id_journal" />', html=True)

        self.assertContains(response,
    r'''<textarea name="title_html" cols="40" rows="10" id="id_title_html">
Complex-scaled multireference configuration-interaction method to study Be and Be-like cations&#39; (B, C, N, O, Mg) Auger resonances 1s2s&lt;SUP&gt;2&lt;/SUP&gt;2p &lt;SUP&gt;1,3&lt;/SUP&gt;P&lt;SUP&gt;o&lt;/SUP&gt;</textarea>''', html=True)
        self.assertContains(response,
    r'''<textarea name="title_latex" cols="40" rows="10" id="id_title_latex">
Complex-scaled multireference configuration-interaction method to study Be and Be-like cations&#39; (B, C, N, O, Mg) Auger resonances 1s2s$^{2}$2p $^{1,3}$P$^{o}$</textarea>''', html=True)
