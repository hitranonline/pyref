from django.test import TestCase


class DOIResolveTest(TestCase):

    def test_resolving_doi_populates_add_reference_page(self):
        doi = '10.1103/PhysRevA.85.032515'
        url = '/refs/resolve/?doi=' + doi
        response = self.client.get(url)
        
        self.assertContains(response,
    r'<input type="text" name="journal" value="Physical Review A" maxlength="500" id="id_journal" />',
                            html=True)
