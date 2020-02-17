#   Copyright 2020 Frances M. Skinner, Christian Hill
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from django.test import TestCase

class DOIResolveTest(TestCase):

    field_template = {}
    field_template['AUTHORS'] = '''<textarea name="authors" cols="40" rows="10" id="id_authors">{}</textarea>'''
    field_template['JOURNAL'] = '''<input type="text" name="journal" value="{}" maxlength="500" id="id_journal" />'''
    field_template['VOLUME'] = '''<input type="text" name="volume" value="{}" maxlength="10" id="id_volume" />'''
    field_template['PAGE_START'] = '''<input type="text" name="page_start" value="{}" maxlength="10" id="id_page_start" />'''
    field_template['PAGE_END'] = '''<input type="text" name="page_end" value="{}" maxlength="10" id="id_page_end" />'''
    field_template['YEAR'] = '''<input type="number" name="year" value="{}" id="id_year" />'''
    field_template['ARTICLE_NUMBER']= '''<input type="text" name="article_number" value="{}" maxlength="16" id="id_article_number" />'''
    field_template['TITLE'] = '''<textarea name="title" cols="40" rows="10" id="id_title">{}</textarea>'''
    field_template['HTML'] = '''<textarea name="title_html" cols="40" rows="10" id="id_title_html">{}</textarea>'''
    field_template['LATEX'] = '''<textarea name="title_latex" cols="40" rows="10" id="id_title_latex">{}</textarea>'''

    def _get_val(self, line):
        return line[line.index('=')+1:].strip()

    def _read_test_dois(self):
        test_dois = {}
        with open('refs/tests/test-dois.txt') as fi:
            for line in fi:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if line.startswith('DOI'):
                    doi = self._get_val(line)
                    test_dois[doi] = {}
                    continue
                for key in DOIResolveTest.field_template.keys():
                    if line.startswith(key):
                        val = self._get_val(line)
                        test_dois[doi][key] = val
                        break
                else:
                    print('Warning: unrecognised key:', key)
        return test_dois


    def test_resolving_doi_populates_add_reference_page(self):
        test_dois = self._read_test_dois()

        for doi, test_fields in test_dois.items():
            url = '/refs/resolve/?doi=' + doi
            response = self.client.get(url)
        
            for key, value in test_fields.items():
                self.assertContains(response,
                   DOIResolveTest.field_template[key].format(value), html=True)
