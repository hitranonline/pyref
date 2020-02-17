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

from django.forms import ModelForm, ValidationError
from .models import Ref

class RefForm(ModelForm):
    class Meta:
        model = Ref
        exclude = ['ris', 'citeproc_json']

    def clean_doi(self):
        doi = self.cleaned_data['doi']
        try:
            ref = Ref.objects.get(doi=doi)
            if ref.pk != self.instance.pk:
                raise ValidationError('A reference with this DOI exists in'
                                            ' the database already')
        except Ref.MultipleObjectsReturned:
            # Hmmm... there are already multiple entries with this DOI in the
            # database. TODO deal with this case
            pass
        except Ref.DoesNotExist:
            # Good: a reference with this DOI is not in the DB already
            pass

        return self.cleaned_data['doi']
